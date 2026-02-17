from openai import OpenAI
from dotenv import load_dotenv
import json

load_dotenv()

client = OpenAI()

   # chain of thought prompting
systemPrompt ='''
        You are an AI assistant who is expert in breaking down the complex problems and then resolve the user query.
        
        For the given user input analyse the input and break down the problem step by step.
        Atleast think 5-6 steps on how to solve the problem before solve it down.
        
        The steps you get a user input, you analyse, you think, you again think several times and then return an output with explaination.

        Follow the steps in sequence that is "analysis","think","output","validate" and finally "result". 
        
        Rules:
        1. Follow the strict JSON output as per Output schema.
        2. Always perform one step at a time and wait for next input.
        3. Carefully analyse the user query.

        Output Format: 
        {{ step: "string", content: "string" }}
        
        Example:
        Input: What is 2 + 2.
        Output: {{ step: "analysis", content: "Alright! the user is interested in maths query and he is asking for basics aithmetic operation."}}
        Output: {{ step: "output", content: "4"}}
        Output: {{ step: "validate", content: "seems like 4 is correct answer for 2 + 2"}}
        Output: {{ step: "result", content: "2 + 2 = 4 and that is calculated by adding all the numbers."}}'''

response = client.chat.completions.create(
    model="gpt-4o",
    response_format={"type": "json_object"},
    messages=[
        { "role": "system", "content": systemPrompt},
        { "role": "user", "content": "What is 3 + 4 * 5"} ,

        { "role": "assistant", "content": json.dumps({"step" : "analyse", "content" : "The query involves both addition and multiplication. According to the order of operations, multiplication should be performed before addition."})},
        { "role": "assistant", "content": json.dumps({"step": "think", "content": "First, we need to perform the multiplication of 4 and 5."})},
        { "role": "assistant", "content": json.dumps({"step": "think", "content": "4 multiplied by 5 equals 20."})},
        { "role": "assistant", "content": json.dumps({"step": "think", "content": "Now that we have the result of the multiplication, which is 20, we need to perform the addition with 3."})},
        { "role": "assistant", "content": json.dumps({"step": "output", "content": "3 + 20 = 23"})},
        { "role": "assistant", "content": json.dumps({"step": "validate", "content": "The calculations seem correct: 3 + (4 * 5) equals 3 + 20, which indeed equals 23."})},
        { "role": "assistant", "content": json.dumps({"step": "result", "content": "The final result of the expression 3 + 4 * 5 is 23, following the order of operations."})},
    ]
)

print(response.choices[0].message.content)