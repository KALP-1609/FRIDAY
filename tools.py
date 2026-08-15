from memory import *
from tavily import TavilyClient
import os

def calculate(expression):
    return eval(expression)

def save_note(note):
    with open('notes.txt', 'a') as f:
        f.write(note + "\n")

    return "Note saved!"

def remember(key,value):
    return save_memory(key=key,value=value)

def recall(key):
    result = get_memory(key=key)
    if result is None:
        return "No memory found!"
    return result

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
def web_search(query):
    response = tavily.search(query=f"latest {query} news article",max_results=1,search_depth="basic")

    results = []

    for result in response["results"]:

        results.append(
            f"Title: {result['title']}\n"
            f"Content: {result['content']}\n"
            f"URL: {result['url']}\n"
        )

    return "\n".join(results)
