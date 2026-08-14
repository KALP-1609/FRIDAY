from dotenv import load_dotenv
from groq import Groq
import os
import json

from tools import *
load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

messages = [{
    "role": "system",
    "content": """
        You are FRIDAY, a personal AI assistant.
        You have access to persistent long-term memory.
        
        IMPORTANT:
        - If the user asks you to remember something, use remember.
        - If the user asks about something that may exist in long-term memory, ALWAYS use recall BEFORE answering.
        - For project-related questions, ALWAYS use the key "project".
        - For name-related questions, ALWAYS use the key "name".
        - For preferences, ALWAYS use the key "preference".
        - Never say you don't know something until you have checked memory.    
    """
}]

print("FRIDAY ONLINE")

tools = [
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Calculate a mathematical expression.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "The expression to evaluate."
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
            "description": "Save a note when the user explicitly asks you to save a note.",
            "parameters": {
                "type": "object",
                "properties": {
                    "note": {
                        "type": "string",
                        "description": "The note to save."
                    }
                },
                "required": ["note"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "remember",
            "description": """
                Store important information in long-term memory.

                Use these standard keys:

                - project
                - name
                - preference
                - general

                Always use the same key for the same type of information.
                """,
            "parameters": {
                "type": "object",
                "properties": {
                    "key": {
                        "type": "string",
                        "description": "The key to store the information under."
                    },
                    "value": {
                        "type": "string",
                        "description": "The information to store."
                    }
                },
                "required": ["key", "value"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "recall",
            "description": """
                Retrieve information from long-term memory.
                
                Use these standard keys:
                - project
                - name
                - preference
                - general
                """,
            "parameters": {
                "type": "object",
                "properties": {
                    "key": {
                        "type": "string",
                        "description": "The key of the memory to retrieve."
                    }
                },
                "required": ["key"]
            }
        }
    }
]

tool_iterations = 0

while tool_iterations < 5:

    tool_iterations += 1

    user_input = input("You: ")

    if user_input.lower() == "quit" or user_input.lower() == "exit":
        print("FRIDAY OFFLINE")
        break
    messages.append({
        "role": "user",
        "content": user_input
    })

    while True:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            tools=tools,
            tool_choice="auto",
            temperature=0
        )
        reply = response.choices[0].message

        if reply.tool_calls:
            messages.append(reply)

            for tool_call in reply.tool_calls:
                function_name = tool_call.function.name

                arguments = json.loads(
                    tool_call.function.arguments
                )

                print("\nTool Called:", function_name)
                print("Arguments:", arguments)

                if function_name == "calculate":
                    result = calculate(
                        arguments["expression"]
                    )
                elif function_name == "save_note":
                    result = save_note(
                        arguments["note"]
                    )
                elif function_name == "remember":
                    result = remember(
                        arguments["key"],
                        arguments["value"]
                    )
                elif function_name == "recall":
                    result = recall(
                        arguments["key"]
                    )
                else:
                    result = "Unknown Tool"

                print("Tool Result:", result)
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": str(result)
                })

            second_response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=messages,
                temperature=0
            )

            assistant_reply = second_response.choices[0].message.content

            messages.append({
                "role": "assistant",
                "content": assistant_reply
            })

            print(f"FRIDAY: {assistant_reply}")

            break