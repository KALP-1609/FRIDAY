import tools
from exceptions import ToolError

tool_registry = {
    "calculate": {
        "function": tools.calculate,
        "description": """
            Evaluate mathematical expressions and calculations.
            Use this tool for arithmetic, percentages, powers, roots,
            logarithms, trigonometric expressions, and other mathematical
            calculations. Do not use Python code or arbitrary function calls.""",
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
        
            Use an appropriate category:
            - identity: information about the user
            - project: information about projects
            - preference: user preferences
            - general: other useful persistent information
        
            Use a descriptive key for the specific fact.
        
            Examples:
            - category: identity, key: name, value: Tony Stark
            - category: project, key: project_name, value: FRIDAY
            - category: preference, key: favorite_show, value: Ultimate-Spider Man
        
            Store information only when the user explicitly asks you to remember it.
            Do not invent, modify, or add information that the user did not provide.
            Store the information as accurately as possible.
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
                },
                "category": {
                    "type": "string",
                    "enum": [
                        "identity","project","preference","general"
                    ],
                    "description": "The category this memory belongs to."
                }
            },
            "required": ["key", "value", "category"]
        }
    },
    "recall": {
        "function": tools.recall,
        "description": """
            Retrieve information from the user's persistent long-term memory.
        
            You MUST use this tool before answering any question that asks about
            information previously stored about the user, including their identity,
            projects, preferences, plans, or other personal information.
        
            For a question about one specific stored fact, provide its key.
        
            For a question asking for multiple stored facts belonging to a category,
            provide the category.
        
            If the user asks what you remember about them generally, retrieve the
            relevant stored memories before answering.
        
            Do not answer memory-related questions from conversation history or
            assumptions.
        
            If no matching memory exists, return that no matching memory was found.
            Do not invent or modify memory information.
        """,
        "parameters": {
            "type": "object",
            "properties": {
                "key": {
                    "type": "string",
                    "description": "The specific memory key to retrieve."
                },
                "category": {
                    "type": "string",
                    "description": "The memory category from which to retrieve matching memories."
                }
            }
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
    if not isinstance(arguments, dict):
        return tool_failure("Tool arguments must be a JSON object.")
    if tool_name not in tool_registry:
        return tool_failure(f"Unknown tool: {tool_name}")

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