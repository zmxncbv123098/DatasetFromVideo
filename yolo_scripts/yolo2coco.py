"""Yolo labels into jsons with backwards bbox transformation.

P.S. in modify_box change your image xywh

"""

import os
import json
from glob import glob
import argparse

def modify_box(box): # TODO image size fix 
    x = float(box[0]) * 2048
    y = float(box[1]) * 2448
    w = float(box[2]) * 2048
    h = float(box[3]) * 2448
    
    x = (x * 2 - w) / 2
    y = (y * 2 - h) / 2
    
    box_new = [round(x, 2), round(y, 2), round(w, 2), round(h, 2)]
    
    return box_new


def create_jsons(input_path, save_path):
    # Read all files
    file_names = glob(input_path + '*.txt')
    
    # Create save directory
    if not os.path.exists(save_path):
        os.makedirs(save_path)
        
    for file in file_names:
        with open(file, 'r') as f:
            lines = f.readlines()
            
        image_name = file.split('/')[-1].split('.txt')[0]
        
        d = {}
        d['image_name'] = image_name + '.jpg'
        d['annotations'] = []
        for line in lines:
            line = line.split()
            camera = {}
            camera['class'] = int(line[0])
            
            box = modify_box(line[1:5])
            camera['box'] = box
            
            if len(line)!=6:
                camera['polygon'] = line[5:-1]
            else:
                camera['polygon'] = None
                
            camera['score'] = round(float(line[-1]), 2)
            
            d['annotations'].append(camera)
        
        # Serializing json
        json_object = json.dumps(d, indent=4)
        
        # Writing to sample.json
        with open(f"{save_path + image_name}.json", "w") as outfile:
            outfile.write(json_object)

def get_args():
    parser = argparse.ArgumentParser("Split Yolo data to train format")
    parser.add_argument(
        "-l",
        "--labels",
        type=str,
        help="Absolute path for the root dir for labels.",
    )

    parser.add_argument(
        "-j",
        "--jsons_path",
        default="",
        type=str,
        help="Output path for jsons ",
    )

    args = parser.parse_args()
    return args

def main(opt):
    labels_dir = opt.images
    jsons_dir = opt.jsons_path

    create_jsons(labels_dir, jsons_dir)


if __name__ == "__main__":
    options = get_args()

    if options.images is not None:
        main(options)
    else:
        input_path = "project/labels"
        save_path = "project/jsons"
    
        create_jsons(input_path, save_path)   