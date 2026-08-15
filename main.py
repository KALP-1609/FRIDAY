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
        - Use remember ONLY when the user explicitly asks you to remember or save information.
        - Use recall ONLY for information about the user or information previously stored in memory.
        - NEVER use recall for general knowledge, factual questions, calculations, explanations, or casual conversation.
        - NEVER use remember unless the user explicitly asks you to remember or save something.
        - For project-related personal information, use the key "project".
        - For name-related personal information, use the key "name".
        - For user preferences, use the key "preference".
        - Answer general knowledge questions directly.
        - When storing information derived from a tool result, store the complete result accurately.
        - Never invent or modify values when creating a memory.
        - Do not create multiple memories for the same request unless the user explicitly asks for multiple separate memories.
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
                Store all information belonging to the same user request as ONE complete memory.
                Do not split one piece of information into multiple memories.
                Do not invent, modify, or add information that the user did not provide.
                Store the information exactly as provided or as directly derived from a tool result.
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
    },
    {
        "type": "function",
        "function": {
            "name": "web_search",
            "description": """
                Search the web for current information, recent events,
                news, facts or information that may have changed recently.
                
                Use this tool only when up to date information is needed.
                Do not use this for general knowledge, factual questions,
                calculations, explanations, or casual conversation which you already know the answer to.
            """,
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The query for which the latest web search results should be retrieved."
                    }
                },
                "required": ["query"]
            }
        }
    }
]

while True:
    user_input = input("You: ")
    if user_input.lower() == "quit" or user_input.lower() == "exit":
        print("FRIDAY OFFLINE")
        break
    messages.append({
        "role": "user",
        "content": user_input
    })

    tool_iterations = 0

    while tool_iterations < 5:
        tool_iterations += 1
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
                arguments = json.loads(tool_call.function.arguments)
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
                elif function_name == "web_search":
                    result = web_search(
                        arguments["query"]
                    )
                else:
                    result = "Unknown Tool"

                print("Tool Result:", result)

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": str(result)
                })

            continue

        assistant_reply = reply.content

        messages.append({
            "role": "assistant",
            "content": assistant_reply
        })

        print(f"FRIDAY: {assistant_reply}")
        break