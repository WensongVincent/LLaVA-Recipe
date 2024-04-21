import json
import os

with open('dataset/recipe1m/finetune-10K-IIM.json') as f:
    data = json.load(f)
pwd = os.getcwd() + '/dataset/recipe1m/'

for d in data:
    d['image'] = pwd + 'images/' + d['image']
