import os
import string
import random
import cv2


class Reader:
    def __init__(self, cap):
        self.cap = cap

    def read(self):
        try:
            _, fr = self.cap.read()
            return fr
        except:
            return None

    def get_information(self):
        return [self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT),
                self.cap.get(cv2.CAP_PROP_FRAME_WIDTH),
                self.cap.get(cv2.CAP_PROP_FPS)]


def get_filelist(directory, ext, separate=False):
    """
    get files list with required extensions

    separate=True creates [[path], [name], [ext]]
    that may be useful is case of work with images/labels files

    Usage:
    imgs_list = get_filelist(dir, ".jpg", True)
    labels_list = get_filelist(dir, ".txt", True)
    for label_name in labels_list[1]:
        id = labels_list[1].index(label_name)
        label_file = os.path.join(labels_list[0][id], label_name + ".txt")
        img_file = os.path.join(imgs_list[0][id], label_name + ".jpg")
    ...
    """

    ret_list = []
    if separate:
        ret_list = [[], [], []]
    for folder, subs, files in os.walk(directory):
        for filename in files:
            if filename.endswith(ext):
                if separate:
                    ret_list[0].append(folder)
                    ret_list[1].append(".".join(filename.split(".")[:-1]))
                    ret_list[2].append(ext)
                else:
                    ret_list.append(os.path.join(folder, filename))
    return ret_list


def get_random_name(name_len=22):
    """generate random name string without extension"""
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(name_len))
