from transformers import AutoTokenizer
from config import MAX_CONTEXT_TOKENS, MAX_REQUEST_TOKENS, SUMMARY_TRIGGER_TOKENS
from conversation import load_summary, save_summary
from conversation_summary import summarize_messages

tokenizer = AutoTokenizer.from_pretrained("openai/gpt-oss-120b")

def message_to_dict(message):
    if isinstance(message, dict):
        return message
    return message.model_dump(exclude_none=True)

def message_tokens(message):
    return estimate_tokens([message])

def estimate_tokens(messages):
    text = ""

    for message in messages:
        message = message_to_dict(message)
        text += str(message.get("role", ""))

        if message.get("content"):
            text += str(message["content"])

        if message.get("tool_calls"):
            text += str(message["tool_calls"])

        if message.get("tool_call_id"):
            text += str(message["tool_call_id"])

        if message.get("name"):
            text += str(message["name"])

    return len(tokenizer.encode(text))

def should_summarize(messages):
    return estimate_tokens(messages) >= SUMMARY_TRIGGER_TOKENS

def context_limit_reached(messages):
    return estimate_tokens(messages) >= MAX_REQUEST_TOKENS

def trim_messages(messages):
    token_count = estimate_tokens(messages)

    if token_count < MAX_REQUEST_TOKENS:
        return messages

    system_message = messages[0]
    conversation = messages[1:]

    while conversation and token_count >= MAX_REQUEST_TOKENS:
        token_count -= message_tokens(conversation.pop(0))

        while conversation and message_to_dict(conversation[0]).get("role") != "user":
            token_count -= message_tokens(conversation.pop(0))

    return [system_message] + conversation

def get_messages_for_summary(messages):
    system_message = messages[0]
    conversation = messages[1:]
    recent_messages = []

    while conversation and len(recent_messages) < 5:
        recent_messages.insert(0, conversation.pop())

    old_messages = []
    token_count = 0

    for message in conversation:
        tokens = message_tokens(message)

        if old_messages and token_count + tokens > 4000:
            break

        old_messages.append(message)
        token_count += tokens

    return system_message, old_messages, recent_messages

def summarize_old_messages(messages):
    system_message, old_messages, recent_messages = get_messages_for_summary(messages)

    if not old_messages:
        return messages

    old_summary = load_summary()

    summary_input = []

    if old_summary:
        summary_input.append({
            "role": "system",
            "content": "Update the existing conversation summary using the new conversation information. Preserve important facts, decisions, tasks, project details, tool results, and relevant context. Do not invent information."
        })
        summary_input.append({
            "role": "user",
            "content": f"Existing summary:\n{old_summary}\n\nNew conversation:\n{old_messages}"
        })
    else:
        summary_input.append({
            "role": "system",
            "content": "Summarize the conversation while preserving important facts, decisions, tasks, project details, tool results, and relevant context. Do not invent information."
        })
        summary_input.append({
            "role": "user",
            "content": str(old_messages)
        })

    summary = summarize_messages(summary_input)
    save_summary(summary)

    return [system_message] + recent_messages