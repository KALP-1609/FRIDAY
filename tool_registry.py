import tools
from exceptions import ToolError

tool_registry = {
    "calculate": {
        "function": tools.calculate,
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
    },
    "save_note": {
        "function": tools.save_note,
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
    },
    "remember": {
        "function": tools.remember,
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
    },
    "recall": {
        "function": tools.recall,
        "description": """
            Retrieve information from the user's persistent long-term memory.
            Use this tool whenever the user asks about information that may have been
            previously stored about them, their projects, preferences, plans, or other
            personal information.
            Do not rely on conversation history to answer these questions.
            Conversation history is not authoritative for persistent memory.
            If the requested information is not stored, return that no matching memory was found.
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
    },
    "web_search": {
        "function": tools.web_search,
        "description": """
            Search the web for current information, recent events,
            news, facts or information that may have changed recently.

            Use this tool only when up to date information is needed.
            Do not use this for general knowledge, factual questions,
            calculations, explanations, or casual conversation.
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
    },
    "read_file": {
        "function": tools.read_file,
        "description": "Read the contents of a text file from the FRIDAY workspace.",
        "parameters": {
            "type": "object",
            "properties": {
                "filename": {
                    "type": "string",
                    "description": "The filename of the file whose contents should be retrieved."
                }
            },
            "required": ["filename"]
        }
    },
    "write_file": {
        "function": tools.write_file,
        "description": """
            Write content to a text file in the FRIDAY workspace.
            Create the file if it does not exist.
            Use the exact filename provided by the user.
        """,
        "parameters": {
            "type": "object",
            "properties": {
                "filename": {
                    "type": "string",
                    "description": "The filename of the file in which the contents needs to be added"
                },
                "content": {
                    "type": "string",
                    "description": "The content to be added to the file"
                }
            },
            "required": ["filename", "content"]
        }
    },
    "list_files": {
        "function": tools.list_files,
        "description": """
            List all files available in the FRIDAY workspace.
            Use this tool when the user asks what files are available.
            Only list files inside the workspace.
        """,
        "parameters": {
            "type": "object",
            "properties": {}
        }
    },
    "read_all_files": {
        "function": tools.read_all_files,
        "description": """
            Read the contents of all files in the FRIDAY workspace.
            Use this when the user explicitly asks to read all files.
            Only access files inside the workspace.
        """,
        "parameters": {
            "type": "object",
            "properties": {}
        }
    }
}

tools_definition = [
    {
        "type": "function",
        "function": {
            "name": name,
            "description": tool["description"],
            "parameters": tool["parameters"]
        }
    }
    for name, tool in tool_registry.items()
]

def execute_tool(tool_name, arguments):
    if tool_name not in tool_registry:
        return tool_failure("Unknown Tool")

    try:
        result = tool_registry[tool_name]["function"](**arguments)
        return tool_success(result)
    except ToolError as e:
        return tool_failure(str(e))
    except Exception as e:
        return tool_failure(f"Unexpected tool error: {e}")

def tool_success(result):
    return {
        "success": True,
        "result": result
    }

def tool_failure(error):
    return {
        "success": False,
        "error": error
    }