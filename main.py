from dotenv import load_dotenv
from groq import Groq, APIError, BadRequestError, RateLimitError
import os
import json

load_dotenv()

from config import *
from tool_registry import *

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

messages = [{
    "role": "system",
    "content": """
        You are FRIDAY, a personal AI assistant.
        
        You have access to persistent long-term memory.
        
        IMPORTANT:
        - Use remember ONLY when the user explicitly asks you to remember or save something.
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
        - When the user asks to read a file, use read_file with the exact filename provided by the user.
        - Tool results are authoritative.
        - When a tool returns information, use that information directly in your response.
        - Never contradict a tool result.
        - Never claim that information is missing when the tool returned it successfully.
        - After answering the user's request, stop. Do not generate additional user messages or conversation turns.
    """
}]

print("FRIDAY ONLINE")

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

    while tool_iterations < MAX_TOOL_ITERATIONS:
        tool_iterations += 1

        try:
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=messages,
                tools=tools_definition,
                tool_choice="auto",
                temperature=TEMPERATURE,
                reasoning_effort="low"
            )

        except RateLimitError:
            print("FRIDAY: API rate limit reached.")
            break

        except BadRequestError as e:
            print(f"FRIDAY: Invalid request: {e}")
            break

        except APIError as e:
            print(f"FRIDAY: API error: {e}")
            break

        except Exception as e:
            print(f"FRIDAY: Unexpected error: {e}")
            break

        reply = response.choices[0].message

        if reply.tool_calls:
            messages.append(reply)

            for tool_call in reply.tool_calls:
                function_name = tool_call.function.name

                try:
                    arguments = json.loads(
                        tool_call.function.arguments
                    )
                except json.JSONDecodeError:
                    result = "Tool Error: Invalid tool arguments."

                    print("\nTool Called:", function_name)
                    print("Tool Result:", result)

                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "name": function_name,
                        "content": result
                    })

                    continue

                print("\nTool Called:", function_name)
                print("Arguments:", arguments)

                result = execute_tool(
                    function_name,
                    arguments
                )

                print("Tool Result:", result)

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": function_name,
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