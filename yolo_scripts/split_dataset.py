import argparse
import pathlib
import random
import shutil
import os
import yaml

def get_args():
    parser = argparse.ArgumentParser("Split Yolo data to train format")
    parser.add_argument(
        "-i",
        "--images",
        type=str,
        help="Absolute path for the root dir for images.",
    )

    parser.add_argument(
        "-l",
        "--labels",
        type=str,
        help="Absolute path for the root dir for yolo labels (should contain classes.txt).",
    )

    parser.add_argument(
        "-o",
        "--output_dir",
        default="yolov5/datasets/YOUR_NEW_YOLO_DATASET",
        type=str,
        help="Name the output dataset directory for Yolov5",
    )

    parser.add_argument(
        "-s",
        "--split",
        nargs="+",
        type=float,
        default=[0.8, 0.1, 0.1],
        help="Split with a ratio. Example [.8, .1, .1]. To only split into training and validation set, set a list to i.e, `(.8, .2)`.",
    )

    parser.add_argument(
        "-e",
        "--ext",
        type=str,
        default="jpg",
        help="Images extension",
    )

    parser.add_argument(
        "--seed",
        type=int,
        default=1337,
        help="Random seed",
    )

    args = parser.parse_args()
    return args


def setup_files(images_dir, seed, ext: str):
    """
    Returns shuffled files
    """
    random.seed(seed)

    files = get_filelist(images_dir, ext)

    files.sort()
    random.shuffle(files)
    return files


def get_filelist(directory: str, ext: str):
    """
    get files list with required extensions list
    """

    ret_list = []
    for folder, subs, files in os.walk(directory):

        for filename in files:

            if filename.split(".")[-1] == ext:
                ret_list.append(os.path.join(folder, filename))

    return ret_list


def split_files(files, split_train_idx, split_val_idx, use_test):
    """
    Splits the files along the provided indices
    """
    files_train = files[:split_train_idx]
    files_val = (
        files[split_train_idx:split_val_idx] if use_test else files[split_train_idx:]
    )

    li = [(files_train, "train"), (files_val, "val")]

    # optional test folder
    if use_test:
        files_test = files[split_val_idx:]
        li.append((files_test, "test"))
    return li


def copy_files(files_type, labels_dir, output, ext):
    """
    Copies the files from the input folder to the output folder
    """
    # get the last part within the file
    for (files, folder_type) in files_type:
        full_path = os.path.join(output, "images", folder_type)
        labels_path = os.path.join(output, "labels", folder_type)
        pathlib.Path(full_path).mkdir(parents=True, exist_ok=True)
        pathlib.Path(labels_path).mkdir(parents=True, exist_ok=True)
        for f in files:
            if type(f) == tuple:
                for x in f:
                    label_name = os.path.split(x)[-1].replace(ext, "txt")
                    shutil.copy2(os.path.join(labels_dir, label_name), labels_path)
                    shutil.copy2(x, full_path)
            else:
                label_name = os.path.split(f)[-1].replace(ext, "txt")
                try:
                    shutil.copy2(os.path.join(labels_dir, label_name), labels_path)
                    shutil.copy2(f, full_path)
                except FileNotFoundError:
                    continue


def split_class_dir_ratio(images_dir, labels_dir, output, ratio, seed, ext):
    files = setup_files(images_dir, seed, ext)

    # the data was shuffled already
    split_train_idx = int(ratio[0] * len(files))
    split_val_idx = split_train_idx + int(ratio[1] * len(files))

    li = split_files(files, split_train_idx, split_val_idx, len(ratio) == 3)
    copy_files(li, labels_dir, output, ext)

    yaml_data = {"path": os.path.join("datasets", os.path.split(output)[-1])}

    yaml_data["train"] = os.path.join(yaml_data["path"], "images", "train")
    yaml_data["val"] = os.path.join(yaml_data["path"], "images", "val")

    if len(ratio) == 3:
        yaml_data["test"] = os.path.join(yaml_data["path"], "images", "test")

    with open(os.path.join(labels_dir, "classes.txt")) as f:
        classes_labels = f.read().splitlines()

    yaml_data["nc"] = len(classes_labels)
    yaml_data["names"] = classes_labels

    with open(os.path.join(output, "dataset.yaml"), 'w') as outfile:
        yaml.dump(yaml_data, outfile, default_flow_style=None)


def main(opt):
    images_dir = opt.images
    labels_dir = opt.labels
    out_dir = opt.output_dir
    ratio = tuple(opt.split)
    seed = opt.seed
    ext = opt.ext

    if os.path.isdir(out_dir):
        raise AssertionError("Oh no! Output directory exists!")

    print("Start split with (train, val, test) = {}".format(ratio))

    split_class_dir_ratio(images_dir, labels_dir, out_dir, ratio, seed, ext)

    print("Finished. Check {}".format(out_dir))


if __name__ == "__main__":
    options = get_args()

    if options.images is not None:
        main(options)
    else:
        print("Processing ... ")
        images_dir = "/var/data/CHPTZ/DATA/plate-detector/pack260722/images"
        labels_dir = "/var/data/CHPTZ/DATA/plate-detector/pack260722/labels_wagon_and_locomotive"
        out_dir = "/home/mbeshkurov/PycharmProjects/LBLPHOTO/yolov5/MY_YOLO/CHTPZ/plate-det-with-locomotive"
        ratio = (0.9, 0.1)
        seed = 1337
        ext = "png"
        split_class_dir_ratio(images_dir, labels_dir, out_dir, ratio, seed, ext)

        print("Done")
