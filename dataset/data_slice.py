import json
import argparse
from tqdm import tqdm
import random
import os
from tqdm import tqdm

'''
this script is used to slice the dataset into smaller sizes
'''

pwd = os.getcwd() + '/'

def merge():
    # this function is used to move the all images to a single folder
    folder_names = list(range(10)) + ["a", "b", "c", "d", "e", "f"]
    count = 0
    for a in folder_names:
        for b in folder_names:
            for c in folder_names:
                for d in folder_names:
                    try:
                        files = os.listdir(f'{pwd}/recipe1m/train/{a}/{b}/{c}/{d}')
                        for f in files:
                            os.rename(f'{pwd}/recipe1m/train/{a}/{b}/{c}/{d}/{f}', f'{pwd}/recipe1m/images/{f}')
                            count += 1
                        files = os.listdir(f'{pwd}/recipe1m/test/{a}/{b}/{c}/{d}')
                        for f in files:
                            os.rename(f'{pwd}/recipe1m/test/{a}/{b}/{c}/{d}/{f}', f'{pwd}/recipe1m/images/{f}')
                            count += 1
                    except:
                        pass
    print(f"Moved {count} files to ./images")

def format_data(data, image_path):
    return {
            'id': image_path[:-4],
            'title': data['title'],
            'ingredients': ','.join([ingredient['text'] for ingredient in data['ingredients']]),
            'instructions': ' '.join([instruction['text'] for instruction in data['instructions']]),
            'path': image_path
        }

def slice_data(layer1, layer2, img_list, size):
    sliced_data = []
    for d in tqdm():
        if len(sliced_data) >= size * 1000:
            break
        # change this if you use the full dataset
        if d['partition'] == 'val':
            continue
        image_path = None
        for info in layer2:
            if info.get('id') == d['id']:
                # randomly select an image from the list of images
                image_path = info['images'][random.randint(0, len(info['images'])-1)]['id']
                break
        if image_path == None:
            continue
        if image_path not in img_list:
            continue
        sliced_data.append(format_data(d, image_path))
    return sliced_data

def main(args):
    if args.merge:
        merge()

    # change this if you use the full dataset
    if args.size > 70:
        print(f"Size {args.size}K is too large, max size is 70K")
        return

    with open(args.input_folder + 'layer1.json', 'r') as f:
        layer1 = json.load(f)
    with open(args.input_folder + 'layer2.json', 'r') as f:
        layer2 = json.load(f)
    
    image_list = os.listdir(args.input_folder + 'images')

    random.shuffle(layer1)

    if args.test_only:
        data = slice_data(reversed(layer1), layer2, image_list, 1)
        with open(args.output_folder + "/test-1K-raw.json", 'w', encoding='utf-8') as json_file:
            json_file.write(json.dumps(data, indent=4))
        print(f"Saved {len(data)} data to {pwd}{args.output_folder}test-1K-raw.json")
        return

    data = slice_data(layer1, layer2, image_list, args.size)
    filename = f'{pwd}{args.output_folder}finetune-{args.size}K-raw.json'
    with open(filename, 'w', encoding='utf-8') as json_file:
        json_file.write(json.dumps(data, indent=4))
    print(f"Saved {len(data)} data to {filename}")


if __name__ == '__main__':
    random.seed(42)
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_folder', type=str, default=pwd+'recipe1m/')
    parser.add_argument('--output_folder', type=str, default=pwd+'recipe1m/')
    parser.add_argument('--size', type=int, default=1, description="Size of the dataset in K")
    parser.add_argument('--test_only', type=bool, default=False)
    parser.add_argument('--merge', type=bool, default=False)
    args = parser.parse_args()
    main(args)
