# This script find missing videos of HACS dataset
# it outputs a file missing.txt, where users can send to developer to request video files

import os
import glob
import csv
import json
import argparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--root_dir', required=True)
    parser.add_argument('--dataset', default='all', choices=['all', 'segments'])
    parser.add_argument('--output_list', default='missing.txt')
    args = parser.parse_args()

    # parse annotation file
    videos_dataset = set()
    if args.dataset == 'all':
        annotation_file = 'HACS_v1.1.1/HACS_clips_v1.1.1.csv'
        with open(annotation_file, 'r') as f:
            reader = csv.reader(f, delimiter=',')
            next(reader)
            for row in reader:
                classname, vid, subset, start, end, label = row
                if subset == 'testing':
                    continue
                classname = classname.replace(' ', '_')
                videos_dataset.add((vid, classname))

    elif args.dataset == 'segments':
        annotation_file = 'HACS_v1.1.1/HACS_segments_v1.1.1.json'
        dataset = json.load(open(annotation_file, 'r'))['database']
        for vid, info in dataset.items():
            info = dataset[vid]
            if info['subset'] == 'testing':
                continue
            annos = info['annotations']
            for anno in annos:
                classname = anno['label'].replace(' ', '_')
                videos_dataset.add((vid, classname))

    print('{} videos in dataset.'.format(len(videos_dataset)))

    # index video files
    video_files = glob.glob(os.path.join(args.root_dir, '**', '*.mp4'), recursive=True)
    videos_exist = set()
    for video in video_files:
        items = video.split('/')
        vid = items[-1][-15:-4]
        classname = items[-2]
        videos_exist.add((vid, classname))

    videos_missing = []
    for item in videos_dataset:
        if item not in videos_exist:
            videos_missing.append(item)
    print('Missing videos:', len(videos_missing))

    if len(videos_missing) > 0:
        # output list to a csv file
        with open(args.output_list, 'w') as f:
            for item in videos_missing:
                f.write('{},{}\n'.format(item[0], item[1]))

    print('Done.')
