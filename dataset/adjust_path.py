import json
import os

with open('./recipe1m/finetune-10K-IIM.json') as f:
    data = json.load(f)
pwd = os.getcwd() + '/recipe1m/'
print(pwd)

for d in data:
    d['image'] = pwd + 'images/' + d['id'] + '.jpg'

with open('./recipe1m/finetune-10K-IIM.json', 'w', encoding='utf-8') as f:
    f.write(json.dumps(data, indent=4))

print(data[0])
