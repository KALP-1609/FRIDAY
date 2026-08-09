from dotenv import load_dotenv
from groq import Groq
import os
import json

from torchgen.api.dispatcher import arguments

from tools import *

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

messages = [{
    "role": "system",
    "content": "You are FRIDAY, a personal AI assistant."
}]

print("FRIDAY ONLINE")

tools = [
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Calculate the sum of two numbers",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "The expression to evaluate"
                    }
                },
                "required": ["expression"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "save_note",
            "description": "Save a note to your memory",
            "parameters": {
                "type": "object",
                "properties": {
                    "note": {
                        "type": "string",
                        "description": "The note to save"
                    }
                },
                "required": ["note"]
            }
        }
    }]

while True:
    user_input = input("You: ")

    if user_input.lower() == "quit" or user_input.lower() == "exit":
        print("FRIDAY OFFLINE")
        break

    messages.append({"role": "user", "content": user_input}) # add user input to local memory

    response = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=messages, tools=tools, tool_choice="auto")

    reply = response.choices[0].message
    if reply.tool_calls:
        tool_call = reply.tool_calls[0]

        function_name = tool_call.function.name

        arguments = json.loads(tool_call.function.arguments)

        if function_name == "calculate" :
            result = calculate(arguments["expression"])
        elif function_name == "save_note" :
            result = save_note(arguments["note"])
        else:
            result = "Unknown Tool"

        print("Tool Result: ", result)

        messages.append({"role": "assistant", "tool_call_id": tool_call.id, "content": str(result)})

        second_response = client.chat.completions.create(model = "llama-3.3-70b-versatile", messages = messages, tools=tools)
        assistant_reply = second_response.choices[0].message
        messages.append({"role": "assistant", "content": assistant_reply.content})

        print(f"FRIDAY: {assistant_reply}")
    else:
        assistant_reply = response.choices[0].message.content
        messages.append({"role": "assistant", "content": assistant_reply})
        print(f"FRIDAY: {assistant_reply}")
