from memory import *
from tavily import TavilyClient
from exceptions import *
import os
import sympy as sp

WORKSPACE_DIR = os.path.abspath("workspace")

# Version 1 tools
def calculate(expression):
    try:
        result = sp.sympify(expression)
        if not result.is_number:

            raise ValueError("Expression must evaluate to a number.")
        return str(result.evalf())
    except Exception as e:
        raise ToolError(f"Calculation failed: {e}")

def save_note(note):
    try:
        with open('notes.txt', 'a') as f:
            f.write(note + "\n")

        return "Note saved!"
    except Exception as e:
        raise FileToolError(f"Failed to save note: {str(e)}")

def remember(key, value, category="general"):
    try:
        return save_memory(
            key=key,
            value=value,
            category=category,
            source="user"
        )
    except Exception as e:
        raise MemoryToolError(f"Failed to save memory: {str(e)}")

def recall(key=None, category=None):
    try:
        if key:
            result = get_memory(key=key)
            if result is None:
                return "No memory found!"
            return result

        if category:
            result = get_memories_by_category(category)
            if not result:
                return "No memories found in this category."
            return result
        raise MemoryToolError(
            "Either a memory key or category must be provided."
        )
    except MemoryToolError:
        raise
    except Exception as e:
        raise MemoryToolError(
            f"Failed to retrieve memory: {str(e)}"
        )

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
        raise ToolError(f"Web Search Failed: {str(e)}")

def get_workspace_path(filename):
    filepath = os.path.abspath(
        os.path.join(WORKSPACE_DIR, filename)
    )

    if not (
            filepath == WORKSPACE_DIR
            or filepath.startswith(WORKSPACE_DIR + os.sep)
    ):
        raise FileToolError("Access denied: path is outside the FRIDAY workspace.")

    return filepath

def read_file(filename):
    filepath = get_workspace_path(filename)

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        raise FileToolError(f"File not found: {filename}")
    except Exception as e:
        raise FileToolError(f"Could not found file: {str(e)}")

def write_file(filename, content):
    filepath = get_workspace_path(filename)

    try:
        with open(filepath, "a", encoding="utf-8") as f:
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