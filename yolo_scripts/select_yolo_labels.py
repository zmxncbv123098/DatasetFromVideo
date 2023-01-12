"""
Select specific yolo labels to generate new labels folder. Then you can use new folder to split data for training.

Usage:
Fill cfg dict with your labels according to your classes.txt file. Comment labels that you want to exclude.

Also, this script providing info about original labels.
"""

import os
import glob


def form_alias_labels(cfg, result_path):
    new_cfg = {}
    count = 0
    classes = []
    for key in cfg.keys():
        new_cfg[key] = count
        count += 1
        classes.append(cfg[key])

    with open(os.path.join(result_path, "classes.txt"), 'w') as f:
        for item in classes:
            f.write("%s\n" % item)

    return new_cfg


def select_lables(cfg, path_labels, result_path):
    print("Sorting ...")

    os.makedirs(result_path, exist_ok=True)

    aliases = form_alias_labels(cfg, result_path)

    lbl = glob.glob(os.path.join(path_labels, "*.txt"))
    for i in lbl:
        res = []
        filename = os.path.split(i)[1]

        if filename == "classes.txt":
            continue

        with open(i, "r") as f:
            lines = f.readlines()

        for j in lines:
            line = j.split(" ")
            if line[0] in cfg:
                line[0] = str(aliases[line[0]])
                res.append(" ".join(line))
        with open(os.path.join(result_path, filename), 'w') as fp:
            for item in res:
                fp.write(item)

    print("Done !")


def labels_stats(labels_path):
    result = {}
    lbl = glob.glob(os.path.join(labels_path, "*.txt"))
    for i in lbl:
        filename = os.path.split(i)[1]
        if filename == "classes.txt":
            continue

        with open(i, "r") as f:
            lines = f.readlines()
        for j in lines:
            lbl = j.split(" ")[0]
            if lbl not in result:
                result[lbl] = 1
            else:
                result[lbl] += 1
    print(result)


if __name__ == "__main__":
    show_stats = True
    apply_select = True
    lables_path = "/var/data/CHPTZ/DATA/auto-layer-capture/pack2/combine_all/labels"
    result_path = "/var/data/CHPTZ/DATA/auto-layer-capture/pack2/combine_all/labels_10012023"


    if show_stats:
        labels_stats(lables_path)

    cfg = {
        "0": "truckbody",
        # "1": "truckbody_upper",
        "2": "truck",
        "3": "grub",
        # "4": "person"
    }

    if apply_select:
        print(f"Labels to select: {', '.join(cfg.values())}")
        select_lables(cfg, lables_path, result_path)
        print(f"New labels stored at {result_path}")
