# few shot prompting

import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
gemini_api_key=os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=gemini_api_key)

response = client.models.generate_content(
    model="gemini-2.5-flash",
    config=types.GenerateContentConfig(
        system_instruction="You are a helpful assistant that speaks like a doctor."
    ), 
    contents="hey tell me some tips!"
)

print(response.text)