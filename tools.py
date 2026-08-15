from memory import *
from tavily import TavilyClient
import os

# Version 1 tools
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

# Version 2 tools
tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
def web_search(query):
    response = tavily.search(query=query,max_results=1,search_depth="basic")

    results = []

    for result in response["results"]:

        results.append(
            f"Title: {result['title']}\n"
            f"Content: {result['content']}\n"
            f"URL: {result['url']}\n"
        )

    return "\n".join(results)

def read_file(filename):
    filepath = os.path.join("workspace", filename)

    if not os.path.abspath(filepath).startswith(os.path.abspath("workspace") + os.sep):
        return "Access denied!"
    try:
        with open(filepath, "r") as f:
            return f.read()
    except FileNotFoundError:
        return "File not found!"
    except Exception as e:
        return f"An error occurred: {str(e)}"

def write_file(filename, content):
    filepath = os.path.join("workspace", filename)

    if not os.path.abspath(filepath).startswith(os.path.abspath("workspace") + os.sep):
        return "Access denied!"
    try:
        with open(filepath, "a") as f:
            f.write("\n" + content)
            return "File written successfully!"
    except Exception as e:
        return f"An error occurred: {str(e)}"

def list_files():
    return [
        file for file in os.listdir("workspace")
        if os.path.isfile(os.path.join("workspace", file))
    ]

def read_all_files():
    files = list_files()
    results = []
    for file in files:
        result = read_file(file)
        results.append(f"{file} --> {result}")

    return "\n".join(results)