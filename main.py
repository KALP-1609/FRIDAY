from dotenv import load_dotenv
from groq import Groq
import os

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

messages = [{
    "role": "system",
    "content": "You are FRIDAY, a personal AI assistant."
}]

print("FRIDAY ONLINE")

while True:
    user_input = input("You: ")

    if user_input.lower() == "quit" or user_input.lower() == "exit":
        print("FRIDAY OFFLINE")
        break

    messages.append({"role": "user", "content": user_input}) # add user input to local memory

    response = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=messages)

    reply = response.choices[0].message.content

    messages.append({"role": "assistant", "content": reply}) # update the local memory with ai response

    print(f"FRIDAY: {reply}") # print response