import llava.myopenai as myopenai
import json
import os
import asyncio
import httpx
import argparse
import base64
from tqdm import tqdm
import time
import sys

pwd = os.getcwd() + '/recipe1m/'

use_iim = False

api_key = ''

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json",
}
endpoint = "https://api.openai.com/v1/chat/completions"

def adpat_prompt(title, ingredients, instructions):
    if use_iim:
        return '''
                You are provided with the name of a food image from a online recipe website. The ingredients and the instructions of the recipe will also be provided to you. Unfortunately, you don't have access to the actual image.
                    
                The name or title of the image is: "{0}".

                The ingredients are as follows: {1}.

                The instructions are as follows: {2}.
                '''.format(title, ingredients, instructions)
    else:
        return '''
                You are provided with the name of a food image from a online recipe website. The ingredients and the instructions of the recipe will NOT be provided to you. Unfortunately, you don't have access to the actual image.
                    
                The name or title of the image is: "{0}".
                '''.format(title)

async def create_chat_completion(mydata, model="gpt-3.5-turbo", temperature=0.6):
    async with httpx.AsyncClient(timeout=None) as client:
        response = await client.post(
            endpoint,
            json={
                "model": model,
                "messages": [
                    {
                        "role": "system", 
                        "content": ''' You are an AI assistant specialized in generating conversations about food related topics.

                        {0}
                        
                        Your task is to generate a conversation between a person (User) inquiring about the image and you (Assistant) responding to their questions. The conversation should proceed as though both the User and Assistant are viewing the image, while not referring to the text information. 

                        Below are requirements for generating the questions and answers in the conversation:
                        - Your answer must follow the format of a conversation between a User and an Assistant.
                        - The answers from Assistant should be at least 4 sentences long. And it should be informative and engaging. But do not exceed 2000 tokens.
                        - Try avoiding that the name of the dish is not mentioned in the conversation if possible.
                        - Do not use phrases like "mentioned", "caption", "context" in the conversation. Instead, refer to the information as being "in the image."
                        - Ensure that questions are diverse and cover a range of visual aspects of the image. For example, questions can be about the appearance, ingredients, preparation method, or serving suggestions of the dish in the image.
                        - The conversation should be engaging and informative, providing interesting details about the dish in the image.
                        - Some questions may involve personal preferences or opinions about the dish, which can be answered based on common knowledge or general food facts.
                        - Some questions may involve comparisons with other dishes or types of cuisine, which can be answered based on general culinary knowledge.
                        - Some questions may ask for recommendations or suggestions related to the dish in the image, which can be answered based on common culinary practices.
                        - Some questions may ask for suitable occasions or settings for the dish in the image, which can be answered based on general food culture.
                        - Some questions may ask for additional information about specific ingredients or cooking techniques used in the dish, which can be answered based on common culinary knowledge.
                        # - The conversation should include 3 to 5 turns of questions and answers about the visual aspects of the image.
                        '''.format(adpat_prompt(mydata['title'], mydata['ingredients'], mydata['instructions'])),
                    },

                ],
                "temperature": temperature,
                "max_tokens": 2048,
            },
            headers=headers,
        )
        return response.json()

async def main(data_list):
    for data in tqdm(data_list):
        conversations = data.get('conversation', None)
        if (conversations is not None) and (len(conversations) > 6):
            continue
        for _ in range(3):
            result = await create_chat_completion(data)
            try:
                data['conversation'] = result['choices'][0]['message']['content']
                break
            except:
                print("Error: ", result)
                print("retrying...")
                time.sleep(0.6)
        if data.get('conversation', None) is None or len(data['conversation']) < 6:
            return

# Run the async main function using asyncio.run only if it's the main module
if __name__ == "__main__":
    # this script is used to generate conversations (only 1K at a time)
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=str)
    parser.add_argument('--output', type=str)
    parser.add_argument('--partition', type=int, default=0)
    parser.add_argument('--iim', type=bool, default=False)
    args = parser.parse_args()
    
    use_iim = args.iim
    if args.iim:
        output_name = pwd + f"{args.output}-IIM-{args.partition}.json"
    else:
        output_name = pwd + f"{args.output}-noIIM-{args.partition}.json"

    if not os.path.exists(output_name):
        with open(pwd + "finetune-25K-raw.json") as f:
            data = json.load(f)
        partition_data = data[args.partition * 1000: (args.partition + 1) * 1000]
        with open(output_name, 'w', encoding='utf-8') as json_file:
            json_file.write(json.dumps(partition_data, indent=4))

    with open(output_name) as f:
        partition_data = json.load(f)
    
    asyncio.run(main(partition_data))
    
    conversation_json = json.dumps(partition_data, indent=4)
    with open(output_name, 'w', encoding='utf-8') as json_file:
        json_file.write(conversation_json)
