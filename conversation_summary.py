from groq import Groq
from dotenv import load_dotenv
from config import MODEL_NAME
import os

load_dotenv()

from conversation import save_summary

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def summarize_messages(messages):
    conversation = ""

    for message in messages:
        role = message.get("role", "")
        if message.get("content"):
            conversation += f"{role}: {message['content']}\n"
        if message.get("tool_calls"):
            conversation += f"{role} tool calls: {message['tool_calls']}\n"
        if message.get("tool_call_id"):
            conversation += f"{role} tool result: {message.get('content', '')}\n"

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": "Summarize the conversation concisely. Preserve important facts, decisions, tasks, project details, and relevant context. Do not invent information."
            },
            {
                "role": "user",
                "content": conversation
            }
        ],
        temperature=0,
        max_completion_tokens=1000
    )

    return response.choices[0].message.content

def create_summary(messages):
    summary = summarize_messages(messages)
    save_summary(summary)
    return summary