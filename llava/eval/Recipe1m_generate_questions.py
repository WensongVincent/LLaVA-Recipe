import json

# The path to the output JSONL file
max_num_img = 300 # test image amount
input_file_path = '/root/LLaVA-Recipe/dataset/recipe1m/test_label/test-1K-IIM-multiround.json' #only used to extract images and imageid
output_file_path = '/root/LLaVA-Recipe/llava/eval/table/Recipe1m_question_recipe_1k_3q.jsonl'

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
                
                # Predefined questions to add in the JSONL file
                questions = [
                    "What recipe can be made with the items in this image?",
                    "How should the food in this picture be prepared?",
                    "What cooking method is used for the food shown in this image?"
                ]
                
                # Write each question as a new line in the JSONL file
                for i, question in enumerate(questions, start=1):
                    # Create the JSONL object
                    jsonl_object = {
                        "image": image_file_name,
                        "question_id": i,
                        "text": question,
                        "category": "generic"
                    }
                    # Write the JSONL object as a line in the file
                    outfile.write(json.dumps(jsonl_object) + '\n')
                
            
            

# Call the function to write the JSONL file
with open(input_file_path, 'r', encoding='utf-8') as infile:
    data = json.load(infile)
    write_jsonl_file(data, output_file_path)

# Return the path to the output file for the user to access
output_file_path


