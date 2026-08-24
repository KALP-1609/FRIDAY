from transformers import AutoTokenizer
from config import MAX_CONTEXT_TOKENS

tokenizer = AutoTokenizer.from_pretrained("openai/gpt-oss-120b",local_files_only=True)

def message_to_dict(message):
    if isinstance(message, dict):
        return message
    return message.model_dump(exclude_none=True)

def message_tokens(message):
    message = message_to_dict(message)
    text = str(message.get("role", ""))

    if message.get("content"):
        text += str(message["content"])

    if message.get("tool_calls"):
        text += str(message["tool_calls"])

    if message.get("tool_call_id"):
        text += str(message["tool_call_id"])

    if message.get("name"):
        text += str(message["name"])

    return len(tokenizer.encode(text))

def estimate_tokens(messages):
    return sum(message_tokens(message) for message in messages)

def context_limit_reached(messages):
    return estimate_tokens(messages) >= MAX_CONTEXT_TOKENS

def trim_messages(messages):
    token_count = estimate_tokens(messages)

    if token_count < MAX_CONTEXT_TOKENS:
        return messages

    system_message = messages[0]
    conversation = messages[1:]
    system_tokens = message_tokens(system_message)

    while conversation and token_count >= MAX_CONTEXT_TOKENS:
        removed_tokens = message_tokens(conversation.pop(0))
        token_count -= removed_tokens

        while conversation and message_to_dict(conversation[0]).get("role") != "user":
            removed_tokens = message_tokens(conversation.pop(0))
            token_count -= removed_tokens

    return [system_message] + conversation