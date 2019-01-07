# HACS-dataset

This project introduces a novel video dataset, named HACS (Human Action Clips and Segments). It consists of two kinds of manual annotations. HACS Clips contains 1.55M 2-second clip annotations; HACS Segments has complete action segments (from action start to end) on 50K videos. The large-scale dataset is effective for pretraining action recognition and localization models, and also serves as a new benchmark for temporal action localization. (*SLAC dataset is now part of HACS dataset.)

## Download Annotation Files
1. Clone this repository:
```
git clone https://github.com/hangzhaomit/HACS-dataset.git
```
2. Unzip annotation files:
```
unzip HACS_v1.1.zip
```
3. Check dataset statistics:
```
python dataset_stats.py
```
&nbsp;&nbsp; You should expect the following output:
```
====Parsing clips====
[training set]: 492753 videos, 1509497 clips
[validation set]: 5982 videos, 20249 clips
[testing set]: 5988 videos, 20296 clips
====Parsing segments====
[training set]: 37618 videos
[validation set]: 5982 videos
[testing set]: 5988 videos
Done.
```

## Annotation File Format
1. For HACS Clips, the annotation file is ```HACS_v1.1/HACS_clips_v1.1.csv```. ```"label": 1```/```"label": -1``` refers to positive/negative sample. The format looks like the following:
```
classname,youtube_id,subset,start,end,label
Archery,a2X2hz1G6i8,training,15.5,17.5,1
Archery,NUdji_CqvcY,training,77.5,79.5,-1
Archery,0O_qMHxBfXg,training,24.5,26.5,-1
...
```

2. For HACS Segments, the annotation file is ```HACS_v1.1/HACS_segments_v1.1.json```, with the same format as ActivityNet dataset:
```
{
  "database": {
    "--0edUL8zmA": {
        "annotations": [
            {"label": "Dodgeball", "segment": [5.40, 11.60]},
            {"label": "Dodgeball", "segment": [12.60, 88.16]},
        "subset": "training",
        "duration": "92.166667",
        "url": "https://www.youtube.com/watch?v=--0edUL8zmA"
    },
  ...
  },
}
```

## Download Videos
1. Install the following libraries:

    (a) youtube-dl (https://github.com/rg3/youtube-dl), make sure it is up-to-date.

    (b) FFmpeg (https://www.ffmpeg.org/).

2. Run the following command to download videos:

```python download_videos.py --root_dir ROOT_DIR [--dataset {all,segments}] [--shortside SHORTSIDE]```

```ROOT_DIR``` is the root path to save the downloaded videos;
You can choose to download all videos or only HACS Segments videos with ```--dataset```;
By default, we resize videos with short side of 256 for less disk usage, you can change with ```--shortside```.

3. Deal with missing videos: (coming soon)

YouTube videos can dissapear over time, so you may find the videos you downloaded incomplete, we provide a solution for you to download missing videos.

## Reference
If you use find the dataset helpful, please cite:
```bibtex
@article{zhao2018hacs,
  title={HACS: Human Action Clips and Segments Dataset for Recognition and Temporal Localization},
  author={Zhao, Hang and Yan, Zhicheng and Torresani, Lorenzo and Torralba, Antonio},
  journal={arXiv preprint arXiv:1712.09374},
  year={2019}
}
```

