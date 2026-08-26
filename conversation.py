import sqlite3
import json
from config import CONVERSATION_HISTORY_LIMIT

DB_NAME = "conversation.db"

def initialize_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    role TEXT NOT NULL,
                    content TEXT,
                    tool_calls TEXT,
                    tool_call_id TEXT,
                    name TEXT
                )
    """)

    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS conversation_summary (
                    id INTEGER PRIMARY KEY CHECK (id = 1),
                    summary TEXT,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
    """)

    conn.commit()
    conn.close()

def save_message(role, content=None, tool_calls=None, tool_call_id=None, name=None):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    if tool_calls is not None:
        tool_calls = json.dumps(tool_calls)

    cursor.execute(
        """
        INSERT INTO messages
            (role, content, tool_calls, tool_call_id, name)
        VALUES (?, ?, ?, ?, ?)
        """,
        (role, content, tool_calls, tool_call_id, name)
    )

    conn.commit()
    conn.close()

def load_messages(limit=CONVERSATION_HISTORY_LIMIT):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT role, content, tool_calls, tool_call_id, name
        FROM (
                 SELECT *
                 FROM messages
                 ORDER BY id DESC
                     LIMIT ?
             )
        ORDER BY id ASC
        """,
        (limit,)
    )

    rows = cursor.fetchall()
    conn.close()

    messages = []

    for role, content, tool_calls, tool_call_id, name in rows:
        message = {
            "role": role
        }

        if content is not None:
            message["content"] = content

        if tool_calls is not None:
            message["tool_calls"] = json.loads(tool_calls)

        if tool_call_id is not None:
            message["tool_call_id"] = tool_call_id

        if name is not None:
            message["name"] = name

        messages.append(message)

    return messages

def clear_conversation():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM messages")

    conn.commit()
    conn.close()

def save_summary(summary):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO conversation_summary (id, summary)
        VALUES (1, ?)
            ON CONFLICT(id)
        DO UPDATE SET
            summary = excluded.summary,
                           updated_at = CURRENT_TIMESTAMP
        """,
        (summary,)
    )

    conn.commit()
    conn.close()

def load_summary():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT summary FROM conversation_summary WHERE id = 1"
    )

    result = cursor.fetchone()
    conn.close()

    return result[0] if result else None