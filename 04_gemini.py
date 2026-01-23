# chain of thoughts

import json
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
gemini_api_key=os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=gemini_api_key)

chat = client.chats.create(
    model="gemini-2.0-flash",
    config=types.GenerateContentConfig(
        system_instruction='''
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
        Output: {{ step: "result", content: "2 + 2 = 4 and that is calculated by adding all the numbers."}}''',
        response_mime_type="application/json"
    ), 
    # contents="what is 3 + 4 * 5"
)

user_query = "what is 3 + 4 * 5"
print(f"User: {user_query}\n")

# Initial message
response = chat.send_message(user_query)

# 3. Create a loop to automatically progress through the steps
while True:
    # Parse the JSON response
    try:
        data = json.loads(response.text)
        print(f"STEP: {data['step']}")
        print(f"CONTENT: {data['content']}\n")
        
        # Stop once the model reaches the "result" step
        if data['step'] == "result":
            break
            
        # Manually trigger the next step by sending a "next" command
        response = chat.send_message("next")
        
    except json.JSONDecodeError:
        print("Error: Model did not return valid JSON.")
        break