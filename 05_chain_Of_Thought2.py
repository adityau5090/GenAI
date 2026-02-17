from openai import OpenAI
from dotenv import load_dotenv
import json

load_dotenv()

client = OpenAI()

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

messages = [
    {"role": "system", "content": systemPrompt},
]

query = input("> ")
messages.append({ "role": "user", "content": query})

while True:
    response = client.chat.completions.create(
        response_format={"type":"json_object"},
        messages=messages,
        model="gpt-4o",
    ) 

    parsed_response= json.loads(response.choices[0].message.content)
    messages.append({ "role": "assistant", "content": json.dumps(parsed_response)})

    if parsed_response.get("step") != "output":
        print(f"🧠: {parsed_response.get("content")}")
        continue
    
    print(f"🤖: {parsed_response.get("content")}")
    break
