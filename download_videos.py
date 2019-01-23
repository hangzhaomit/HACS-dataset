# This script downloads and resize HACS dataset
# using an open source downloader (https://github.com/rg3/youtube-dl)
# and FFMPEG (https://www.ffmpeg.org)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import shutil
import subprocess
import random
import json
import csv
import argparse
from multiprocessing import Pool
from functools import partial


def download_to_tmp(vid, tmp_video):
    url = 'https://www.youtube.com/watch?v={}'.format(vid)
    cmd = ['youtube-dl', '-q', '-f', 'mp4', '-o', tmp_video, url]
    subprocess.call(cmd)


def probe_res(video):
    # probe the resolution of video
    command = ["ffprobe",
               "-loglevel",  "quiet",
               "-select_streams", "v:0",
               "-show_entries", "stream=height,width",
               "-print_format", "json",
               "-show_format",
               video]
    pipe = subprocess.Popen(command,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT)
    out, err = pipe.communicate()
    vmeta = json.loads(out)
    wid = int(vmeta['streams'][0]['width'])
    hei = int(vmeta['streams'][0]['height'])
    return wid, hei


def resize_move(tmp_video, resized_video, shortside=256):
    wid, hei = probe_res(tmp_video)

    if (wid > shortside) and (hei > shortside):
        if wid >= hei:
            hei_new = shortside
            wid_new = int(1. * wid / hei * shortside)
            wid_new = int(wid_new/2)*2
        else:
            wid_new = shortside
            hei_new = int(1. * hei / wid * shortside)
            hei_new = int(hei_new/2)*2

        command = ["ffmpeg",
                   "-y",
                   "-loglevel",  "quiet",
                   "-i", tmp_video,
                   "-vf", "scale={}x{}".format(wid_new, hei_new),
                   "-c:a", "copy",
                   resized_video]
        subprocess.call(command)
        os.remove(tmp_video)
    else:
        shutil.move(tmp_video, resized_video)


def process(video, args):
    vid, classname = video
    basename = 'v_{}.mp4'.format(vid)
    folder = os.path.join(args.root_dir, classname)
    if not os.path.isdir(folder):
        os.mkdir(folder)
    tmp_video = os.path.join(args.tmp_dir, basename)
    resized_video = os.path.join(folder, basename)
    if os.path.exists(resized_video):
        return

    try:
        download_to_tmp(vid, tmp_video)
        resize_move(tmp_video, resized_video, args.shortside)
        print('Processed [{}/{}]'.format(classname, vid))
    except Exception as e:
        print('Error processing [{}/{}]: {}'.format(classname, vid, e))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--root_dir', required=True)
    parser.add_argument('--tmp_dir', default='/tmp/HACS')
    parser.add_argument('--dataset', default='all', choices=['all', 'segments'])
    parser.add_argument('--shortside', default=256, type=int)
    parser.add_argument('--num_worker', default=16, type=int)
    parser.add_argument('--seed', default=123, type=int)
    args = parser.parse_args()
    random.seed(args.seed)

    # make dataset dirs
    if not os.path.isdir(args.root_dir):
        os.mkdir(args.root_dir)
    if not os.path.isdir(args.tmp_dir):
        os.mkdir(args.tmp_dir)

    # parse annotation file
    videos = set()
    if args.dataset == 'all':
        annotation_file = 'HACS_v1.1/HACS_clips_v1.1.csv'
        with open(annotation_file, 'r') as f:
            reader = csv.reader(f, delimiter=',')
            next(reader)
            for row in reader:
                classname, vid, subset, start, end, label = row
                if subset == 'testing':
                    continue
                classname = classname.replace(' ', '_')
                videos.add((vid, classname))

    elif args.dataset == 'segments':
        annotation_file = 'HACS_v1.1/HACS_segments_v1.1.json'
        dataset = json.load(open(annotation_file, 'r'))['database']
        for vid, info in dataset.items():
            info = dataset[vid]
            if info['subset'] == 'testing':
                continue
            annos = info['annotations']
            for anno in annos:
                classname = anno['label'].replace(' ', '_')
                videos.add((vid, classname))

    print('{} videos to download.'.format(len(videos)))

    # download with process pool
    videos = list(videos)
    random.shuffle(videos)
    if args.num_worker > 1:
        pool = Pool(args.num_worker)
        pool.map(partial(process, args=args), videos)
    else:
        for video in videos:
            process(video, args)

    print('Completed!')
