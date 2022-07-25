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

1. Create following file structure if you want to make screenshots from multiple videos:
    - base_folder
      - raw
        - your_videos
2. In `screenshot_from_video.py` edit all necessary variables, look for:
- `videos_dir`
- `file_extension`
- `skip_to`
3. Run `screenshot_from_video.py`.

**Or use argparse**
3. 
```bash
    python screenshot_from_video.py --videos "/path/to/videos/" --ext ".mp4" --skip "3:14:15" 
    ```
    
    or if you want only one video to procces 
    
    ```bash
    python screenshot_from_video.py --videos "/path/to/video.mp4" --ext ".mp4" --skip "3:14:15"
    ```

4. The script will automatically create folder dataset in "some_folder", where your photos will be.
    - base_folder
      - raw
        - your_videos
      - dataset
        - your_images


### Bonus Scripts
- `select_yolo_labels.py` - Select specific yolo labels to generate new labels folder. Then you can use new folder to split data for training.
- `split_dataset.py` - Splitting dataset and preparing to train YoloV5.
- `mkv_to_mp4.py` - Convert mkv files to mp4 
- `opencv_build.txt` - Helpful file if you want to build opencv-python from source. For example: if you want to use h264 (*avc1) codec for videos.

**For more info use --help flag or check the files.**
