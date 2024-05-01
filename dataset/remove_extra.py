import json
import os
import argparse
from tqdm import tqdm

'''
this script is used to delete extra images that are not in the dataset
'''

def delete_extra(args):
    if args.are_you_sure:
        image_list = []
        with open("./recipe1m/finetune-10K-raw.json") as f:
            data = json.load(f)
            image_list.extend([d['path'] for d in data])
        with open("./recipe1m/finetune-25K-raw.json") as f:
            data = json.load(f)
            image_list.extend([d['path'] for d in data])
        with open("./recipe1m/test-1K-raw.json") as f:
            data = json.load(f)
            image_list.extend([d['path'] for d in data])
        image_list = list(set(image_list))

        # uncomment this to delete extra images
        # for d in tqdm(os.listdir("./recipe1m/images/")):
        #     if d not in image_list:
        #         os.remove(f"./recipe1m/images/{d}")
        
        print("Deleted extra images")
        print(f'the number of target images are {len(image_list)}')
        print(f'the number of remaining images are {len(os.listdir("./recipe1m/images/"))}')
    else:
        print("you are not sure")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--are_you_sure', type=bool, default=False)
    args = parser.parse_args()
    delete_extra(args)
