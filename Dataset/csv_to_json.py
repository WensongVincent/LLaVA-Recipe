import csv
import json
import os
import argparse
import random

def data_process(dataset):
    pwd = os.getcwd() + '/'
    csv_file_path = pwd + dataset + '/data.csv'
    json_file_path = pwd + dataset
    path_prefix = pwd + dataset + '/images/'
    random.seed(42)
    # Initialize an empty list to hold the JSON data
    data = []
    prompts = [
        "<image>\nCould you guide me on how to prepare the dish displayed in this image?",
        "<image>\nI'm intrigued by the meal in this picture. Can you explain how to cook it?",
        "<image>\nWhat's the recipe for the food shown in this photo?",
        "<image>\nHow do I make the dish that's in this image?",
        "<image>\nCould you provide the cooking steps for the meal depicted here?",
        "<image>\nWhat are the instructions to replicate the dish shown in the picture?",
        "<image>\nCan you help me understand how to cook what's in this photo?",
        "<image>\nHow is the food in this image prepared?",
        "<image>\nWhat's the method for cooking the dish pictured here?",
        "<image>\nI'd love to try making the food in this picture. How do I do that?",
    ]

    num_train = 9429
    num_val = 12123
    
    # Open the CSV file for reading
    with open(csv_file_path, mode='r', encoding='utf-8') as csv_file:
        # Create a CSV reader object
        csv_reader = csv.DictReader(csv_file)
        
        # Loop through each row in the CSV file
        count = 0
        for row in csv_reader:
            # Extract and format data from the CSV row
            count += 1
            image_name = row['Image_Name']
            id_value = image_name  # Assuming Image_Name can serve as a unique ID; adjust if necessary
            image_value = f"{path_prefix}{image_name}.jpg"
            if os.path.isfile(image_value) is False:
                continue
            if count < num_train:
                conversations = [
                    {
                        "from": "human",
                        "value": prompts[random.randint(0,9)]
                    },
                    {
                        "from": "gpt",
                        # "value": f"{row['Ingredients']} {row['Instructions']}"
                        "value": f"{row['Instructions']}"
                    }
                ]
            else:
                conversations = [
                    {
                        "from": "human",
                        "value": prompts[random.randint(0,9)]
                    },
                    {
                        "from": "gpt",
                        "value": f"{row['Ingredients']} {row['Instructions']}"
                        # "value": f"{row['Instructions']}"
                    }
                ]
            
            
            # Construct the JSON object for this row
            json_object = {
                "id": id_value,
                "image": image_value,
                "conversations": conversations
            }
            
            # Append the JSON object to our data list
            data.append(json_object)

    # Serialize the list of JSON objects to a JSON string
    
    # todo: change this in other dataset
    train, val, test = data[:num_train], data[num_train:num_val], data[num_val:] # only for 200m dataset
    random.shuffle(train)
    random.shuffle(val)
    random.shuffle(test)
    train_json = json.dumps(train, ensure_ascii=False, indent=4)
    val_json = json.dumps(val, ensure_ascii=False, indent=4)
    test_json = json.dumps(test, ensure_ascii=False, indent=4)

    # Write the JSON string to the output file
    with open(json_file_path + '/train.json', mode='w', encoding='utf-8') as json_file:
        json_file.write(train_json)
    with open(json_file_path + '/val.json', mode='w', encoding='utf-8') as json_file:
        json_file.write(val_json)
    with open(json_file_path + '/test.json', mode='w', encoding='utf-8') as json_file:
        json_file.write(test_json)

    print(f"{len(data)} data")
    print(len(train), len(val), len(test))
    print("CSV has been converted to JSON successfully.")

parser = argparse.ArgumentParser(description='argparse', formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('--dataset', '-d', help='name of dataset', default='dataset-200m')
args = parser.parse_args()

if __name__ == '__main__':
    try:
        data_process(args.dataset)
    except Exception as e:
        print(e)
