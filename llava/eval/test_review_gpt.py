import argparse
import json
import os
import time


from openai import OpenAI
client = OpenAI(api_key=OPENAI_API_KEY)

# completion = client.chat.completions.create(
#   model="gpt-3.5-turbo",
#   messages=[
#     {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
#     {"role": "user", "content": "Compose a poem that explains the concept of recursion in programming."}
#   ]
# )

# print(completion.choices[0].message)

questions = [{"image": "7a4833e18e.jpg", "question_id": 1, "text": "What recipe can be made with the items in this image?", "category": "generic"}
            ]

answer1 = [{"image": "7a4833e18e.jpg", "question_id": 1, "prompt": "What recipe can be made with the items in this image?", "text": "The image shows a combination of ingredients that can be used to create a delightful treat. You can use these ingredients to make a delicious cupcake with a unique twist.", "answer_id": "QrtY4HUY7yBXsqq64ENrnp", "model_id": "llava-lora-7b-10K-IIM-e1", "metadata": {}}
           ]

answer2 = [{"image": "7a4833e18e.jpg", "question_id": 1, "prompt": "What recipe can be made with the items in this image?", "text": "The image features a cupcake with a blackberry on top, sitting on a blue table. To make a cupcake with a blackberry on top, you would need the following ingredients: cupcake batter, blackberries, powdered sugar, and a cupcake liner. You can either bake the cupcake batter in a cupcake pan or use a muffin tin to create the cupcake. Once the cupcake is baked, you can remove it from the pan and let it cool. Then, you can top the cupcake with a blackberry, and sprinkle powdered sugar on top. Finally, you can place the cupcake in a cupcake liner and serve it. This recipe is a simple and delicious way to enjoy a cupcake with a touch of fruit flavor.", "answer_id": "VuikWmHYQo7kZBDoqVRhbL", "model_id": "llava-v1.5-7b", "metadata": {}}
           ]

roles = ['Assistant']
prompts = ["We would like to request your feedback on the performance of two AI assistants in response to the user question displayed later.\nPlease rate the helpfulness, relevance, accuracy, level of details of their responses. Each assistant receives an overall score on a scale of 1 to 10, where a higher score indicates better overall performance.\nPlease first output a single line containing only two values indicating the scores for Assistant 1 and 2, respectively. The two scores are separated by a space.\nIn the subsequent line, please provide a comprehensive explanation of your evaluation, avoiding any potential bias and ensuring that the order in which the responses were presented does not affect your judgment."]

contexts = ["Wild Blackberry Vanilla Cupcakes. Ingredients: 1 cup Unsalted Butter, Room Temperature,1-23 cup Granulated Sugar,4 whole Eggs,1 Tablespoon Vanilla Extract,3 cups All-purpose Flour,1 Tablespoon Baking Powder,1/2 teaspoons Baking Soda,1- 1/4 cup Buttermilk,2 cups Blackberries,2 cups (or As Needed) Buttercream Icing, Your Preference,Sanding Sugar, As Needed. Instructions: Preheat oven to 350 degrees F (180 degrees C). In a mixer bowl fitted with a paddle attachment, beat butter with sugar until light and fluffy (a few minutes). Beat in eggs, one at a time, beating well after each addition. Beat in vanilla. Whisk together flour, baking powder, baking soda and salt. Stir dry mixture into wet (butter) mixture alternately with buttermilk, making 3 additions of dry ingredients and 3 of buttermilk. Fold in blackberries. Using an ice cream scoop or 1/4-cup measurer, scoop batter into a muffin tin lined with cupcake liners. Bake for approximately 15-20 minutes, until cake tester (toothpicks or skewers work well too) inserted in centre comes out clean. Let cool in muffin tins for about 5 minutes, then remove and let cool completely before adding icing. Pipe a swirl of icing on top of cupcake, and roll the iced cupcakes in a bowl of sanding sugar. Top with a blackberry or decoration of choice and enjoy! Note: You can find a vanilla buttercream icing recipe in my recipe box."]

NUM_SECONDS_TO_SLEEP = 0.5

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
      
for ques, ans1, ans2, role, prompt, context in zip(questions, answer1, answer2, roles, prompts, contexts):
    content = (f'[Context]\n{context}\n\n'
               f'[Question]\n{ques["text"]}\n\n'
               f'[{role} 1]\n{ans1["text"]}\n\n[End of {role} 1]\n\n'
               f'[{role} 2]\n{ans2["text"]}\n\n[End of {role} 2]\n\n'
               f'[System]\n{prompt}\n\n'
               )
    print(content)
    review = get_eval(content, max_tokens=1024)
    print(review)
    scores = parse_score(review)
    print(scores)




