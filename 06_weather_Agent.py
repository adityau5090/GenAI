from openai import OpenAI
from dotenv import load_dotenv
import requests
import json

load_dotenv()

client = OpenAI()

def get_weather(city: str):
    print("tool called: get_weather ", city)
    url = f"https://wttr.in/{city}?format=%C+%t%22"
    response = requests.get(url, timeout=20)

    if response.status_code == 200:
        return f"The weather in {city} is {response.text}"
    return "Tool is not working"

avaliable_tools = {
    "get_weather": {
        "fn": get_weather,
        "description": "Takes a city name as an input and returns the current weather for city"
    }
}

system_prompt = f"""
You are an helpuful AI assistant who is specialized in resolving user query.
You work on start, plan, action, observe mode.
For the given user query and available tools paln the step-by-step execution based on planning , slect the revelant tool from the available tool and based on tool selection you perform an action to call the tool.
Wait for the observation and based on observation from the tool call resolve the user query.

Rules:
1. Follow the strict JSON output as Output Schema
2. Always perform one step at a time and wait for next input
3. carefully analyze the use query

Output JSON format:
{{
  "step": "string",
  "content": "string",
  "function": "The name of the function if the step is action"
  "input" : "The input parameter for the function"  
}}

Available tools: 
- get_weather: Takes a city name as an input and returns the current weather for city


Example:
Input:"What is the weather of new york?
Output: {{ "step": "plan", "content": "The user is interested in weather data of new york" }}
Output: {{ "step": "plan", "content": "From the available I should call get_weather" }}
Output: {{ "step": "action", "function": "get_weather", "input": "new york" }}
Output: {{ "step": "observe", "output": "10 Degree Cel" }}
Output: {{ "step": "output", "content": "The weather of New York seems to be 10 degrees" }}
"""


messages = [
    { "role" : "system", "content": system_prompt},
]

userQuery = input("> ")
messages.append({ "role": "user", "content": userQuery })

while True:
    response = client.chat.completions.create(
    model="gpt-4o",
    response_format={"type": "json_object"},
    messages=messages
    )

    parsed_response = json.loads(response.choices[0].message.content)
    messages.append({"role":"assistant", "content": json.dumps(parsed_response)})

    if parsed_response.get("step") == "plan":
        print(f"🧠: {parsed_response.get("content")}")
        continue

    if parsed_response.get("step") == "action":
        tool_name = parsed_response.get("function")
        tool_input = parsed_response.get("input")

        if avaliable_tools.get(tool_name, False) != False:
            output = avaliable_tools[tool_name].get("fn")(tool_input)
            messages.append({ "role": "assistant", "content": json.dumps({ "step": "observe", "output": output})})
            continue


    if parsed_response.get("step") == "output":
        print(f"🤖: {parsed_response.get("content")}")
        break
    