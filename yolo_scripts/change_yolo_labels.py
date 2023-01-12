import os
import glob

def change_labels(labels_dir, new_labels_dir, classes):

    os.makedirs(new_labels_dir, exist_ok=True)

    txts = glob.glob(os.path.join(labels_dir, "*.txt"))

    if os.path.isfile(os.path.join(labels_dir, "classes.txt")):
        with open(os.path.join(labels_dir, "classes.txt"), 'r') as f:
            txt_labels = f.readlines()
        print("\033[93mChange following classes:\033[0m")
        for i in classes:
            print(f"{i}->{classes[i]} : {txt_labels[int(i)]} --> {txt_labels[int(classes[i])]}".replace("\n", ""))

        if input("\033[93mContinue? (y/n)\033[0m\n") == "y":
            pass
        else:
            exit(1)
    else:
        if input("\033[93m[WARNING]: No classes.txt file. Continue? (y/n)\033[0m\n") == "y":

            print("Change following classes:")
            for i in classes:
                print(f"{i}->{classes[i]}")
        else:
            exit(1)

    print("START NEW DATASET CREATION..")

    for n, t in enumerate(txts):
        print(f"\r{n + 1}/{len(txts)} {t}", end="")

        if "classes" in t or "test.txt" in t or "train.txt" in t or "scenes" in t:
            continue

        with open(t) as f:
            labels = f.readlines()

        labels_new = ""
        for l in labels:
            l = l.split()
            if l[0] in classes:
                l[0] = classes[l[0]]
                labels_new += f"{l[0]} {l[1]} {l[2]} {l[3]} {l[4]}\n"
            else:
                labels_new += f"{l[0]} {l[1]} {l[2]} {l[3]} {l[4]}\n"

        new_txt_file = t.replace(labels_dir, new_labels_dir)

        txt_save_dir = "/".join(new_txt_file.split("/")[:-1])

        if not os.path.isdir(txt_save_dir):
            os.makedirs(txt_save_dir)

        with open(new_txt_file, "w") as f:
            f.write(labels_new)

if __name__ == "__main__":
    labels_dir = "/home/mikhail/Рабочий стол/del/DATA/labels_truckbody_grub"
    new_labels_dir = "/home/mikhail/Рабочий стол/del/DATA/labels_grub_1to2_label"

    classes_to_replace = {
        "1": "2", # replace class 1 with class 2
    }

    change_labels(labels_dir, new_labels_dir, classes_to_replace)