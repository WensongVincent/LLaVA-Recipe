import json
import random

# The path to the output JSONL file
random.seed(42)
max_num_img = 100 # test image amount
input_file_path = 'change this' #only used to extract images and imageid
output_file_path = 'change this'

# preset questions
# 0-9 for ingredients
# 10-19 for instructions
questions = [
    "Could you tell me what ingredients are used in this dish?",
    "What are the main components of this recipe?",
    "Can you list the ingredients that make up this meal?",
    "I'm curious about the ingredients in this picture; what are they?",
    "What items are needed to prepare this dish as shown in the image?",
    "Could you detail the ingredients used in this cuisine depicted here?",
    "What goes into making this dish that's pictured?",
    "I'd like to know the ingredients of this food; what are they?",
    "Can you help me identify what's in this dish from the image?",
    "What are all the elements included in this dish shown in the picture?",
    "Could you guide me on how to prepare the dish displayed in this image?",
    "I'm intrigued by the meal in this picture. Can you explain how to cook it?",
    "What's the recipe for the food shown in this photo?",
    "How do I make the dish that's in this image?",
    "Could you provide the cooking steps for the meal depicted here?",
    "What are the instructions to replicate the dish shown in the picture?",
    "Can you help me understand how to cook what's in this photo?",
    "How is the food in this image prepared?",
    "What's the method for cooking the dish pictured here?",
    "I'd love to try making the food in this picture. How do I do that?",
]

# Function to write the JSONL file from the provided JSON data
def write_jsonl_file(json_data, output_file_path):

    num_img = 0
    # Open the output file in write mode
    with open(output_file_path, 'w', encoding='utf-8') as outfile:
        # Iterate over the items in the JSON data
        for item in json_data:
            if num_img < max_num_img:
                num_img += 1
                # Extract the image ID from the 'id' field
                image_id = item['id']
                # Extract the image file name from the 'image' field
                image_file_name = item['image'].split('/')[-1]
                
                # Randomly select two questions
                Q1_id, Q2_id = random.randint(1, 10), random.randint(11, 20)

                # Qestions for ingredients
                jsonl_object = {
                    "image": image_file_name,
                    "question_id": Q1_id,
                    "text": questions[Q1_id-1],
                    "category": "generic"
                }
                outfile.write(json.dumps(jsonl_object) + '\n')
                jsonl_object = {
                    "image": image_file_name,
                    "question_id": Q2_id,
                    "text": questions[Q2_id-1],
                    "category": "generic"
                }
                outfile.write(json.dumps(jsonl_object) + '\n')
                
                # a random question from conversation
                idx = random.randint(0, len(item['conversations']) / 2 - 1)
                questions.append(item['conversations'][idx * 2]['value'].split('\n')[-1])
                jsonl_object = {
                    "image": image_file_name,
                    "question_id": len(questions),
                    "text": questions[-1],
                    "category": "generic"
                }
                outfile.write(json.dumps(jsonl_object) + '\n')
                
# Call the function to write the JSONL file
with open(input_file_path, 'r', encoding='utf-8') as infile:
    data = json.load(infile)
    write_jsonl_file(data, output_file_path)

# Return the path to the output file for the user to access
output_file_path
