import csv
import json

file_clips = './HACS_v1.1/HACS_clips_v1.1.csv'
file_segments = './HACS_v1.1/HACS_segments_v1.1.json'
subsets = ['training', 'validation', 'testing']


# HACS Clips statistics
def parse_clips():
    print('====Parsing clips====')

    videos = {subset: set() for subset in subsets}
    n_clips = {subset: 0 for subset in subsets}

    with open(file_clips, 'r') as f:
        reader = csv.reader(f, delimiter=',')
        next(reader)
        for row in reader:
            classname, vid, subset, start, end, label = row
            videos[subset].add(vid)
            n_clips[subset] += 1

    for subset in subsets:
        print('[{} set]: {} videos, {} clips'.format(
              subset, len(videos[subset]), n_clips[subset]))

# HACS Segments statistics
def parse_segments():
    print('====Parsing segments====')
    dataset_segments = json.load(open(file_segments, 'r'))['database']
    n_videos = {subset: 0 for subset in subsets}
    # n_segments = {subset: 0 for subset in subsets}

    for vid, info in dataset_segments.items():
        subset = info['subset']
        n_videos[subset] += 1
        # n_segments[subset] += len(info['annotations'])

    for subset in subsets:
        print('[{} set]: {} videos'.format(
              subset, n_videos[subset]))


if __name__ == '__main__':
    parse_clips()
    parse_segments()
    print('Done.')
