from dotenv import load_dotenv
from groq import Groq, APIError, BadRequestError, RateLimitError
import os
import json

load_dotenv()

from config import *
from tool_registry import *
from conversation import *
from memory import get_all_memories

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

messages = [{
    "role": "system",
    "content": """
        You are FRIDAY, a personal AI assistant.

        You have access to persistent long-term memory.

        MEMORY RULES:
        - Persistent memory is the authoritative source for information about the user.
        - Conversation history is NOT a source of truth for persistent user information.
        - If the user asks about information that may have been previously stored about them, use recall before answering.
        - Never answer a question about stored user information solely from conversation history.
        - If recall returns information, use that result directly.
        - If recall returns no memory, say that the information is not currently stored.
        - Do not invent personal information.

        REMEMBER RULES:
        - Use remember ONLY when the user explicitly asks you to remember or save information.
        - Store the complete information provided by the user.
        - Do not split one request into multiple memories unless necessary.
        - Never modify or invent information being stored.
        
        GENERAL RULES:
        - Answer general knowledge questions directly.
        - Use tools when they are necessary.
        - Tool results are authoritative.
        - Never contradict a successful tool result.
        - After answering the user's request, stop.
    """
}]

def refres_memory_context():
    base_prompt = messages[0]["content"].split("\n\nCURRENT PERSISTENT MEMORY:")[0]
    memories = get_all_memories()
    memory_context = ""

    if memories:
        memory_context = "\n\nCURRENT PERSISTENT MEMORY:\n"
        for key,value in memories.items():
            memory_context += f"- {key}: {value}\n"
    messages[0]["content"] = base_prompt + memory_context

initialize_database()

refres_memory_context()

messages.extend(load_messages())

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
    save_message("user",user_input)

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

                if function_name == "remember":
                    refres_memory_context()

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
        save_message("assistant",assistant_reply)
        print(f"FRIDAY: {assistant_reply}")
        break