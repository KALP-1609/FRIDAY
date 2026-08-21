import sqlite3

DATABASE = 'memory.db'

def create_database():
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            key TEXT UNIQUE NOT NULL,
            value TEXT NOT NULL
            )
    """)

    connection.commit()
    connection.close()

def save_memory(key, value):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    cursor.execute("""
                INSERT INTO memory (key, value)
                VALUES (?, ?)
                ON CONFLICT(key)
                DO UPDATE SET value = excluded.value
    """, (key, value))

    connection.commit()
    connection.close()

    return "memory saved!"

def get_memory(key):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    cursor.execute(
        "SELECT value FROM memory WHERE key = ?",
        (key,)
    )
    result = cursor.fetchone()
    connection.close()
    return result[0] if result else None

def get_all_memories():
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("SELECT key, value FROM memory")

    results = cursor.fetchall()
    connection.close()

    return {
        key: value
        for key, value in results
    }