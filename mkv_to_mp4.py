from functions import *

import os
import cv2


def write_video(filename, reader_class, frames_per_sec, show=False):
    frames_per_sec = max(1, frames_per_sec)
    out = None

    try:
        while True:
            frame = reader_class.read()
            if show:
                cv2.imshow('video', frame)

            if not out:
                height, width, channels = frame.shape
                fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                out = cv2.VideoWriter(filename, fourcc, frames_per_sec, (width, height))
            if frame is None:
                break

            out.write(frame)

    finally:
        out and out.release()
        cv2.destroyAllWindows()


videos_dir = "/home/mikhail/PycharmProjects/DatasetFromVideo/test"
videos_list = sorted(get_filelist(os.path.join(videos_dir, "raw"), ext=".mkv"))

for n, _ in enumerate(videos_list):
    video = videos_list[n]
    print("%s/%s  |  %s" % (n+1, len(videos_list), video))
    save_filename = video.replace(".mkv", ".mp4")

    reader = Reader(cv2.VideoCapture(video))
    h, w, fps = reader.get_information()

    write_video(save_filename, reader, fps)

    if os.path.exists(video):
        os.remove(video)
        print(video, "removed")
    else:
        print("The file does not exist")
