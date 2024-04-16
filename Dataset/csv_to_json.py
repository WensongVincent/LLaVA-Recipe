import csv
import json
import os
import argparse

def data_process(dataset):
    pwd = os.getcwd() + '/'
    csv_file_path = pwd + dataset + '/data.csv'
    json_file_path = pwd + dataset + '/data.json'
    path_prefix = pwd + dataset + '/images'

    # Initialize an empty list to hold the JSON data
    data = []

    # Open the CSV file for reading
    with open(csv_file_path, mode='r', encoding='utf-8') as csv_file:
        # Create a CSV reader object
        csv_reader = csv.DictReader(csv_file)
        
        # Loop through each row in the CSV file
        for row in csv_reader:
            # Extract and format data from the CSV row
            image_name = row['Image_Name']
            id_value = image_name  # Assuming Image_Name can serve as a unique ID; adjust if necessary
            image_value = f"{path_prefix}{image_name}.jpg"
            conversations = [
                {
                    "from": "human",
                    "value": "<image>\nHow can I cook it?"
                },
                {
                    "from": "gpt",
                    "value": f"{row['Ingredients']} {row['Instructions']}"
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
    json_data = json.dumps(data, ensure_ascii=False, indent=4)

    # Write the JSON string to the output file
    with open(json_file_path, mode='w', encoding='utf-8') as json_file:
        json_file.write(json_data)

    print("CSV has been converted to JSON successfully.")

parser = argparse.ArgumentParser(description='argparse', formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('--dataset', '-d', help='name of dataset', default='dataset-200m')
args = parser.parse_args()

if __name__ == '__main__':
    try:
        data_process(args.dataset)
    except Exception as e:
        print(e)
