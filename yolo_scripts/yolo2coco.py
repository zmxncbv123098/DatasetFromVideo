"""Yolo лейблы в jsons
"""

import os
import json
from glob import glob


def modify_box(box):
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



if __name__ == "__main__":
  input_path = "project/labels"
  save_path = "project/jsons"
  
  create_jsons(input_path, save_path)