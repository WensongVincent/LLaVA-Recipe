import argparse
import json
import os
import time
import numpy as np
from tqdm import tqdm

OPENAI_API_KEY=None #Add openai key here
NUM_SECONDS_TO_SLEEP = 0.5
ROLE = 'Assistant'
PROMPT = "We would like to request your feedback on the performance of two AI assistants in response to the user question displayed later.\nPlease rate the helpfulness, relevance, accuracy, level of details of their responses. Each assistant receives an overall score on a scale of 1 to 10, where a higher score indicates better overall performance.\nPlease first output a single line containing only two values indicating the scores for Assistant 1 and 2, respectively. The two scores are separated by a space.\nIn the subsequent line, please provide a comprehensive explanation of your evaluation, avoiding any potential bias and ensuring that the order in which the responses were presented does not affect your judgment."

from openai import OpenAI
client = OpenAI(api_key=OPENAI_API_KEY)

## Test section
# completion = client.chat.completions.create(
#   model="gpt-3.5-turbo",
#   messages=[
#     {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
#     {"role": "user", "content": "Compose a poem that explains the concept of recursion in programming."}
#   ]
# )

# print(completion.choices[0].message)

def get_eval(content: str, max_tokens: int):
    while True:
        try:
            response = client.chat.completions.create(
                model='gpt-3.5-turbo',
                messages=[{
                    'role': 'system',
                    'content': 'You are a helpful and precise assistant for checking the quality of the answer.'
                }, {
                    'role': 'user',
                    'content': content,
                }],
                temperature=0.2,  # TODO: figure out which temperature is best for evaluation
                max_tokens=max_tokens,
            )
            break
        # except client.chat.error.RateLimitError:
        #     pass
        except Exception as e:
            print(e)
        time.sleep(NUM_SECONDS_TO_SLEEP)

    return response.choices[0].message.content
  
def parse_score(review):
    try:
        score_pair = review.split('\n')[0]
        score_pair = score_pair.replace(',', ' ')
        sp = score_pair.split(' ')
        if len(sp) == 2:
            return [float(sp[0]), float(sp[1])]
        else:
            print('error', review)
            return [-1, -1]
    except Exception as e:
        print(e)
        print('error', review)
        return [-1, -1]
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='ChatGPT VQA evaluation')
    parser.add_argument('-q', '--question')
    parser.add_argument('-c', '--context')
    parser.add_argument('-a', '--answer-list', nargs='+', default=[])
    parser.add_argument('-o', '--output')
    parser.add_argument('--max-tokens', type=int, default=1024, help='maximum number of tokens produced in the output')
    parser.add_argument('')
    args = parser.parse_args()
    
    # Get paths
    questions_path = args.question
    answer1_path = args.answer_list[0]
    answer2_path = args.answer_list[1]
    contexts_path = args.context
    output_path = args.output
    
    # Get output
    if os.path.isfile(os.path.expanduser(args.output)):
        cur_reviews = [json.loads(line) for line in open(os.path.expanduser(args.output))]
    else:
        cur_reviews = []

    review_file = open(f'{args.output}', 'a')
    
    # Role of answer
    role = ROLE

    # GPT prompt
    prompt = PROMPT
    
    # Get questions
    questions = []
    with open(questions_path, 'r') as file:
        for lines in file:
            data = json.loads(lines)
            questions.append(data)
    # print(questions)
    # print(len(questions))
    
    # Get Answer 1
    answer1 = []
    with open(answer1_path, 'r') as file:
        for lines in file:
            data = json.loads(lines)
            answer1.append(data)
    # print(answer1)
    # print(len(answer1))
    
    # Get Answer 2
    answer2 = []
    with open(answer2_path, 'r') as file:
        for lines in file:
            data = json.loads(lines)
            answer2.append(data)
    # print(answer2)
    # print(len(answer2))
    

    # Get Contexts
    contexts = []
    with open(contexts_path, 'r') as file:
        all_data = json.load(file)
        for data in all_data:
            context = 'dish name: ' + data['title'] + '.\n' + 'Ingredients: ' + data['ingredients'] + '.\n' + 'Instructions: ' + data['instructions'] + '.'
            contexts.append(context)
    # print(contexts)
    # print(len(contexts))
    # print(contexts[0])
    
    # import pdb; pdb.set_trace()
    
    # Evaluate
    reviews = []
    scores = []
    num_eval = 2
    for ques, ans1, ans2, context in tqdm(zip(questions[:num_eval], answer1[:num_eval], answer2[:num_eval], contexts[:num_eval]), total=num_eval, desc="Evaluating"):
        content = (f'[Context]\n{context}\n\n'
                f'[Question]\n{ques["text"]}\n\n'
                f'[{role} 2]\n{ans2["text"]}\n\n[End of {role} 2]\n\n'
                f'[{role} 1]\n{ans1["text"]}\n\n[End of {role} 1]\n\n'
                f'[System]\n{prompt}\n\n'
                )
        cur_js = {
            'image': ques['image'],
            'question_id': ques['question_id'],
            'answer1_id': ans1.get('answer_id', ans1['question_id']),
            'answer2_id': ans2.get('answer_id', ans2['answer_id']),
        }
        review = get_eval(content, max_tokens=1024)
        score = parse_score(review)
        reviews.append(review)
        scores.append(score)
        
        cur_js['content'] = review
        cur_js['tuple'] = scores
        review_file.write(json.dumps(cur_js) + '\n')
        review_file.flush()
        # print(review)
    # print(len(reviews))

    scores = np.array(scores)
    avg = np.mean(scores, axis=0)
    print(f"Ours: {avg[0]} / 10 \nLLaVA-7B: {avg[1]} / 10")