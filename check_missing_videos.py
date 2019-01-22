import os
import fnmatch
import csv
import json
import argparse


def find_recursive(root_dir, ext='.mp4'):
    files = []
    for root, dirnames, filenames in os.walk(root_dir):
        for filename in fnmatch.filter(filenames, '*' + ext):
            files.append(os.path.join(root, filename))
    return files


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--root_dir', required=True)
    parser.add_argument('--dataset', default='all', choices=['all', 'segments'])
    parser.add_argument('--output_list', default='missing.csv')
    args = parser.parse_args()

    # parse annotation file
    vids_dataset = set()
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
                vids_dataset.add(vid)

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
                vids_dataset.add(vid)

    print('{} videos in dataset.'.format(len(vids_dataset)))

    # index video files
    video_files = find_recursive(args.root_dir)
    vids_exist = [os.path.basename(video)[2:-4] for video in video_files]
    vids_exist = set(vids_exist)

    vids_missing = []
    for vid in vids_dataset:
        if vid not in vids_exist:
            vids_missing.append(vid)
    print('Missing videos:', len(vids_missing))

    # output list to a csv file
    with open(args.output_list, 'w') as f:
        for vid in vids_missing:
            f.write('{}\n'.format(vid))

    print('Done.')
