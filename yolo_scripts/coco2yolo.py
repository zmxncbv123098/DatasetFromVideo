""" COCO JSON into bbox or segments labels (.txt)
"""
import json
import os
from selectors import EpollSelector
import numpy as np
import argparse

def get_img_ann(image_id, data):
    img_ann = []
    isFound = False
    for ann in data['annotations']:
        if ann['image_id'] == image_id:
            img_ann.append(ann)
            isFound = True
    if isFound:
        return img_ann
    else:
        return None


def get_img(filename, data):
    for img in data['images']:
        if img['file_name'] == filename:
            return img


def create_labels(input_images, input_json, output_labels, label_type):
    os.makedirs(output_labels, exist_ok=True)
    file_names = os.listdir(input_images)
    print(len(file_names))

    # Reading Annotations file
    f = open(input_json)
    data = json.load(f)
    f.close()

    # Applying Conversion
    count = 0
    for filename in file_names:
        # Extracting image
        img = get_img(filename, data)
        img_id = img['id']
        img_w = img['width']
        img_h = img['height']

        # Get Annotations for this image
        img_ann = get_img_ann(img_id, data)

        if img_ann:
            # Opening file for current image
            file_object = open(f"{output_labels}/{filename.split('.jpg')[0]}.txt", "a")

            for ann in img_ann:
                current_category = ann[
                                       'category_id'] - 1  # Subtracting 1 from category id because class labels in yolo format starts from 0.

                if label_type == 'box':
                    current_bbox = ann['bbox']
                    x = current_bbox[0]
                    y = current_bbox[1]
                    w = current_bbox[2]
                    h = current_bbox[3]

                    # Finding midpoints
                    x_centre = (x + (x + w)) / 2
                    y_centre = (y + (y + h)) / 2

                    # Normalization
                    x_centre = x_centre / img_w
                    y_centre = y_centre / img_h
                    w = w / img_w
                    h = h / img_h

                    # Limiting upto fix number of decimal places
                    x_centre = format(x_centre, '.6f')
                    y_centre = format(y_centre, '.6f')
                    w = format(w, '.6f')
                    h = format(h, '.6f')

                    # Writing current object
                    file_object.write(f"{current_category} {x_centre} {y_centre} {w} {h}\n")

                else:
                    s = [j for i in ann['segmentation'] for j in i]  # all segments concatenated
                    s = (np.array(s).reshape(-1, 2) / np.array([img_w, img_h])).reshape(-1).tolist()

                    file_object.write(f"{current_category} {' '.join(str(x) for x in s)}\n")

            file_object.close()
        count += 1

def get_args():
    parser = argparse.ArgumentParser("Split Yolo data to train format")
    parser.add_argument(
        "-i",
        "--images",
        type=str,
        help="Absolute path for the root dir for images.",
    )

    parser.add_argument(
        "-j",
        "--json",
        type=str,
        help="Absolute path for the coco json",
    )

    parser.add_argument(
        "-o",
        "--output_dir",
        default="./yolo_labels",
        type=str,
        help="Output path for yolo labels",
    )

    parser.add_argument(
        "-t",
        "--type",
        default='box',
        type=str,
        help="mask or box"
    )

    args = parser.parse_args()
    return args

def main(opt):
    images_dir = opt.images
    json_path = opt.json
    out_dir = opt.output_dir
    type = opt.type

    create_labels(images_dir, json_path, out_dir, label_type=type)

if __name__ == "__main__":
    options = get_args()

    if options.images is not None:
        main(options)
    else:

        input_images = "path/to/images"
        input_json = "path/to/coco/json"
        output_labels = "save/labels/path"
        type = 'mask' # box

        create_labels(input_images, input_json, output_labels, label_type='mask')
