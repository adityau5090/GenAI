from openai import OpenAI
from dotenv import load_dotenv
import os
import json
import subprocess

load_dotenv()

client = OpenAI()

def run(command):
    output = subprocess.getoutput(command)
    return output


available_tools = {
    "run": {
        "fn": run,
        "description": "Execute terminal command"
    }
}

system_prompt = """
You are a helpful AI assistant who runs terminal commands.

You MUST always return valid JSON.

Output schema:

Step 1 (plan):
{"step":"plan","content":"what you will do"}

Step 2 (action):
{"step":"action","function":"run","input":"terminal command"}

Step 3 (observe):
(This will be provided by system)

Final step:
{"step":"output","content":"final answer"}

Rules:
1. Only JSON, no extra text.
2. One step at a time.
3. Wait for observation before next step.
"""

messages = [
    {"role": "system", "content": system_prompt}
]

while True:
    user_query = input("> ")
    messages.append({"role": "user", "content": user_query})

    while True:

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            response_format={"type": "json_object"},
            messages=messages,
        )

        parsed_response = json.loads(response.choices[0].message.content)
        print(parsed_response)

        messages.append({
            "role": "assistant",
            "content": json.dumps(parsed_response)
        })

        step = parsed_response.get("step")

        if step == "plan":
            print(f"🧠: {parsed_response.get('content')}")
            continue

        if step == "action":
            tool_name = parsed_response.get("function")
            command = parsed_response.get("input")

            if tool_name in available_tools:
                output = available_tools[tool_name]["fn"](command)

                messages.append({
                    "role": "assistant",
                    "content": json.dumps({
                        "step": "observe",
                        "output": output
                    })
                })
            continue

        if step == "output":
            print(f"🤖: {parsed_response.get('content')}")
            break
