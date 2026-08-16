import tools
from exceptions import ToolError

tools_definition = [
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
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": """
                Read the contents of a text file from the FRIDAY workspace.
            """,
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
        }
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
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
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_files",
            "description": """
                List all files available in the FRIDAY workspace.
                Use this tool when the user asks what files are available,
                what files exist, or wants to see the contents of the workspace directory.
                Only list files inside the workspace.
                Do not access files outside the workspace.
            """,
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_all_files",
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
]

tool_mapping = {
    "calculate": tools.calculate,
    "save_note": tools.save_note,
    "remember": tools.remember,
    "recall": tools.recall,
    "web_search": tools.web_search,
    "read_file": tools.read_file,
    "write_file": tools.write_file,
    "list_files": tools.list_files,
    "read_all_files": tools.read_all_files
}

def execute_tool(tool_name, arguments):
    if tool_name not in tool_mapping:
        return "Tool Error: Unknown Tool"
    try:
        return tool_mapping[tool_name](**arguments)
    except ToolError as e:
        return f"Tool Error: {e}"
    except Exception as e:
        return f"Unexpected tool error: {e}"