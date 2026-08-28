import sqlite3
from datetime import datetime

DATABASE = "memory.db"


def get_connection():
    return sqlite3.connect(DATABASE)

def create_database():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
           CREATE TABLE IF NOT EXISTS memory (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 category TEXT NOT NULL,
                 key TEXT UNIQUE NOT NULL,
                 value TEXT NOT NULL,
                 source TEXT NOT NULL DEFAULT 'user',
                 created_at TEXT NOT NULL,
                 updated_at TEXT NOT NULL
   )
   """)

    connection.commit()
    connection.close()

def save_memory(key, value, category="general", source="user"):
    connection = get_connection()
    cursor = connection.cursor()

    now = datetime.now().isoformat()

    cursor.execute("""
                   INSERT INTO memory (category,key,value,source,created_at,updated_at)
                   VALUES (?, ?, ?, ?, ?, ?)
                   ON CONFLICT(key)
                   DO UPDATE SET
                      value = excluded.value,
                      category = excluded.category,
                      source = excluded.source,
                      updated_at = excluded.updated_at
                   """, (category,key,value,source,now,now))

    connection.commit()
    connection.close()

    return "memory saved!"

def get_memory(key):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""SELECT value FROM memory WHERE key = ?""", (key,))

    result = cursor.fetchone()
    connection.close()
    return result[0] if result else None

def get_all_memories():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
       SELECT category, key, value, source, created_at, updated_at
       FROM memory
       ORDER BY updated_at DESC
    """)

    results = cursor.fetchall()
    connection.close()
    return [
        {
            "category": category,
            "key": key,
            "value": value,
            "source": source,
            "created_at": created_at,
            "updated_at": updated_at
        }
        for category, key, value, source, created_at, updated_at in results
    ]

def delete_memory(key):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
                   DELETE FROM memory
                   WHERE key = ?
                   """, (key,))

    deleted = cursor.rowcount > 0

    connection.commit()
    connection.close()

    return deleted

def get_memories_by_category(category):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
                   SELECT category, key, value, source, created_at, updated_at
                   FROM memory
                   WHERE category = ?
                   ORDER BY updated_at DESC
                   """, (category,))

    results = cursor.fetchall()
    connection.close()

    return [
        {
            "category": category,
            "key": key,
            "value": value,
            "source": source,
            "created_at": created_at,
            "updated_at": updated_at
        }
        for category, key, value, source, created_at, updated_at in results
    ]