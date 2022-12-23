# Create dataset from videos

You want to create a dataset from videos?

Then, may be, this code will help you. Cheers!

### Install the Requirements
- `pip install -r requierments.txt`

### Hotkeys
| Key    | Purpose                 |
|--------|-------------------------|
| P      | Play/Pause video        |
| Z/X    | Rewind +/- 60 frames    |
| C/V    | Rewind +/- 3 frames     | 
| B/N    | Rewind +/- 600 frames   | 
| U/I    | Rewind +/- 10000 frames |
| . or , | Next/Previous video     |
| S      | Save Frame              |
| D      | Delete last saved frame |

### Usage

1. In `screenshot_from_video.py` edit all necessary variables, look for:
- `data_path` - may be path/to/folder with videos **or** path/to/video.ext
- `file_extension` - file/files extension
- `skip_to` - if video is too long u can skip via timecode
2. Run `screenshot_from_video.py`.

**Or use argparse**

3. Execute in bash

```bash
python screenshot_from_video.py --videos "/path/to/videos/" --ext ".mp4" --skip "3:14:15" 
```
    
or if you want only one video to procces 

```bash
python screenshot_from_video.py --videos "/path/to/video.mp4" --ext ".mp4" --skip "3:14:15"
```

4. The script will automatically create folder dataset in "some_folder", where your photos will be.
    - base_folder
      - your_video(s)
      - dataset
        - your_images


# Bonus Scripts
- `yolo_scripts/select_yolo_labels.py` - Select specific yolo labels to generate new labels folder. Then you can use new folder to split data for training.
- `yolo_scripts/split_dataset.py` - Splitting dataset and preparing to train YoloV5.
- `yolo_scripts/coco2yolo.py` - Converts COCO annotation json to yolo labels.
- `yolo_scripts/yolo2coco.py` - Converts yolo label back to readible json with backwards bbox transformation.

- `yolo_scripts/coco_json_parser.py` - Useful tool to prepare your data after markup. <b>For more info check the file</b>

- `mkv_to_mp4.py` - Convert mkv files to mp4 
- `opencv_build.txt` - Helpful file if you want to build opencv-python from source. For example: if you want to use h264 (*avc1) codec for videos.

**For more info use --help flag or check the files.**
