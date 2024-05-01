import json
import os
from tqdm import tqdm

count = 0
data, res = [], []
for i in range(25):
    with open(f"./recipe1m/finetune-25K-{i}.json") as f:
        data.extend(json.load(f))

# with open(f"./recipe1m/test-1K-IIM.json") as f:
#     data.extend(json.load(f))

def format_conversation(d):
    formated = []
    global count
    conversations = d.get('conversation', None)
    if conversations is None:
        print(d['id'])
        print(d['title'])
        exit()
    conversations = conversations.rstrip('\n').split("\n")
    
    haha = 0
    for c in conversations:
        if c.startswith("User:"):
            formated.append({
                "from": "human",
                "value": c[6:]
            })
            haha += 1
        elif c.startswith("Assistant:"):
            formated.append({
                "from": "gpt",
                "value": c[11:]
            })
            haha -= 1
        elif (len(c) > 0):
            print(d['id'])
            print(d['title'])
            exit()
            
    
    if len((formated)) < 6 or haha != 0:
        print(d['id'])
        print(d['title'])
        exit()
    formated[0]['value'] = "<image>\n" + formated[0]['value']
    
    return formated

for d in tqdm(data):
    res.append({
        "id": d['id'],
        "image": os.getcwd()+ "/recipe1m/images/" + d['path'],
        "conversations": format_conversation(d)
    })
    
    
with open("./recipe1m/finetune-25K.json", 'w') as f:
    f.write(json.dumps(res, indent=4))
# with open("./recipe1m/test-1K-IIM.json", 'w') as f:
#     f.write(json.dumps(res, indent=4))
print(len(res))
print(count)
