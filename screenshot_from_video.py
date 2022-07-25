from functions import *
import argparse
import cv2
"""

Z/X - Перемотка на +/- 60 кадров 
C/V - Перемотка на +/- 3 кадров
B/N - Перемотка на +/- 600 кадров
,/. - Предыдущее/Следующее видео

S - Сохранить фрэйм
D - Удалить последний сохранённый фрейм

Q - Закончить просмотр
"""


def get_args():
    parser = argparse.ArgumentParser("Screenshots from video-stream")
    parser.add_argument(
        "-v",
        "--videos",
        type=str,
        help="Absolute path for the root dir with 'raw' folder.",
    )

    parser.add_argument(
        "-e",
        "--ext",
        type=str,
        default=".mp4",
        help="Videos extension",
    )

    parser.add_argument(
        "-s",
        "--skip",
        type=str,
        default="",
        help="Skip videos to start from another time. Format - \"hh:mm:ss\"",
    )

    args = parser.parse_args()
    return args


def main(data_path, file_extension, skip_to=""):

    if file_extension in data_path:
        save_path = os.path.join(os.path.split(data_path)[0], "dataset")
        videos_list = [data_path]
    else:
        save_path = os.path.join(data_path, "dataset")
        videos_list = sorted(get_filelist(os.path.join(data_path, "raw"), ext=file_extension))

    last_saved = None
    waitKey_mode = 0

    os.makedirs(save_path, exist_ok=True)

    # Счётчик для сохранённых фреймов
    counter = 0
    already_saved_imgs = get_filelist(save_path, ".jpg")
    for img_name in already_saved_imgs:
        counter = max(counter, int(img_name.split("_")[-1].replace(".jpg", ""))) + 1

    video_id = 0
    for n, _ in enumerate(videos_list):
        video = videos_list[video_id]

        reader = Reader(cv2.VideoCapture(video))

        frames = int(reader.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        print(video, "frames total:", frames)

        if skip_to:
            h, m, s = map(int, skip_to.split(":"))
            fps = int(reader.cap.get(cv2.CAP_PROP_FPS))
            frame_skip_id = (((h * 60) + m) * 60) * fps
            reader.cap.set(propId=cv2.CAP_PROP_POS_FRAMES, value=int(frame_skip_id))

        while True:

            frame = reader.read()

            if frame is None:
                break

            frame_id = int(reader.cap.get(cv2.CAP_PROP_POS_FRAMES))

            save_img = frame.copy()

            cv2.putText(frame, "frame {}/{}".format(frame_id, frames),
                        (5, frame.shape[0] - 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 5)

            cv2.namedWindow("image", cv2.WINDOW_NORMAL)
            cv2.imshow("image", frame)

            key = cv2.waitKey(waitKey_mode) & 0xff
            if key == ord('p'):
                if waitKey_mode == 0:
                    waitKey_mode = 1
                    print("- play")
                elif waitKey_mode == 1:
                    waitKey_mode = 0
                    print("- pause")

            # Перемотка назад на -1 кадр
            if key == ord('c'):
                reader.cap.set(propId=cv2.CAP_PROP_POS_FRAMES, value=int(reader.cap.get(cv2.CAP_PROP_POS_FRAMES)) - 3)

            # Перемотка вперед на +1 кадр
            if key == ord('v'):
                reader.cap.set(propId=cv2.CAP_PROP_POS_FRAMES, value=int(reader.cap.get(cv2.CAP_PROP_POS_FRAMES)) + 3)

            # Перемотка назад на -n кадров
            if key == ord('z'):
                reader.cap.set(propId=cv2.CAP_PROP_POS_FRAMES, value=int(reader.cap.get(cv2.CAP_PROP_POS_FRAMES)) - 60)

            # Перемотка вперед на +n кадров
            if key == ord('x'):
                reader.cap.set(propId=cv2.CAP_PROP_POS_FRAMES, value=int(reader.cap.get(cv2.CAP_PROP_POS_FRAMES)) + 60)

            # Перемотка назад на -n кадров
            if key == ord('b'):
                reader.cap.set(propId=cv2.CAP_PROP_POS_FRAMES, value=int(reader.cap.get(cv2.CAP_PROP_POS_FRAMES)) - 600)

            # Перемотка вперед на +n кадров
            if key == ord('n'):
                reader.cap.set(propId=cv2.CAP_PROP_POS_FRAMES, value=int(reader.cap.get(cv2.CAP_PROP_POS_FRAMES)) + 600)

            # Перемотка назад на -n кадров
            if key == ord('i'):
                reader.cap.set(propId=cv2.CAP_PROP_POS_FRAMES, value=int(reader.cap.get(cv2.CAP_PROP_POS_FRAMES)) - 10000)

            # Перемотка вперед на +n кадров
            if key == ord('u'):
                reader.cap.set(propId=cv2.CAP_PROP_POS_FRAMES, value=int(reader.cap.get(cv2.CAP_PROP_POS_FRAMES)) + 10000)

            # Предыдущее видео
            if key == ord(','):
                video_id = video_id - 2
                break

            # Следующее видео
            if key == ord('.'):
                break

            # Сохранить фрейм
            if key == ord('s'):
                save_name = "{}_{}.jpg".format(video.split("/")[-1].replace(file_extension, ""), counter)
                last_saved = os.path.join(save_path, save_name)
                print("- img saved to {}".format(os.path.join(save_path, save_name)))
                cv2.imwrite(os.path.join(save_path, save_name), save_img)
                counter += 1

            # Удалить последний сохраненный фрейм
            if key == ord('d'):
                try:
                    os.remove(last_saved)
                    print("- {} deleted".format(last_saved))
                except:
                    print("- Can`t delete {}".format(last_saved))

            if key == ord('q'):
                print("Aborting")
                exit(1)

        video_id += 1
        print()


if __name__ == "__main__":
    # Папка с исходными видео с соответствующим расширением
    # data_path = "/path/to/folder_with_raw"
    data_path = "/path/to/video_file.avi"
    file_extension = ".avi"
    skip_to = ""

    options = get_args()
    if options.videos is not None:
        main(options.videos, options.ext, skip_to=options.skip)
    else:
        main(data_path, file_extension, skip_to="2:28:20")
