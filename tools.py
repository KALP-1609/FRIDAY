from memory import *
from tavily import TavilyClient
from exceptions import *
import os

# Version 1 tools
def calculate(expression):
    try:
        return str(eval(expression))
    except Exception as e:
        raise ToolError(f"Calculation failed: {str(e)}")

def save_note(note):
    try:
        with open('notes.txt', 'a') as f:
            f.write(note + "\n")

        return "Note saved!"
    except Exception as e:
        raise FileToolError(f"Failed to save note: {str(e)}")

def remember(key,value):
    try:
        return save_memory(key=key,value=value)
    except Exception as e:
        raise MemoryToolError(f"Failed to save memory: {str(e)}")

def recall(key):
    try:
        result = get_memory(key=key)
        if result is None:
            return "No memory found!"
        return result
    except Exception as e:
        raise MemoryToolError(f"Failed to retrieve memory: {str(e)}")

# Version 2 tools
tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
def web_search(query):
    try:
        response = tavily.search(query=query,max_results=1,search_depth="basic")

        results = []

        for result in response["results"]:

            results.append(
                f"Title: {result['title']}\n"
                f"Content: {result['content']}\n"
                f"URL: {result['url']}\n"
            )

        return "\n".join(results)
    except Exception as e:
        raise MemoryToolError(f"Failed to retrieve memory: {str(e)}")

def read_file(filename):
    filepath = os.path.join("workspace", filename)

    if not os.path.abspath(filepath).startswith(os.path.abspath("workspace") + os.sep):
        return "Access denied!"
    try:
        with open(filepath, "r") as f:
            return f.read()
    except FileNotFoundError:
        raise FileToolError(f"File not found: {filename}")
    except Exception as e:
        raise FileToolError(f"Could not found file: {str(e)}")

def write_file(filename, content):
    filepath = os.path.join("workspace", filename)

    if not os.path.abspath(filepath).startswith(os.path.abspath("workspace") + os.sep):
        return "Access denied!"
    try:
        with open(filepath, "a") as f:
            f.write("\n" + content)
            return "File written successfully!"
    except Exception as e:
        raise FileToolError(f"Could not write file: {str(e)}")

def list_files():
    try:
        return [
            file for file in os.listdir("workspace")
            if os.path.isfile(os.path.join("workspace", file))
        ]
    except Exception as e:
        raise FileToolError(f"Could not list files: {str(e)}")

def read_all_files():
    try:
        files = list_files()
        results = []
        for file in files:
            result = read_file(file)
            results.append(f"{file} --> {result}")

        return "\n".join(results)
    except Exception as e:
        raise FileToolError(f"Could not read files: {str(e)}")