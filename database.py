import sqlite3

DB_NAME = "database.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def init_db():
    conn = get_connection()

    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS channels(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        telegram_id INTEGER UNIQUE,
        title TEXT,
        send_time TEXT DEFAULT '09:00',
        enabled INTEGER DEFAULT 1
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS events(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        channel_id INTEGER,
        title TEXT,
        event_date TEXT,
        emoji TEXT DEFAULT '🎂'
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS settings(
        id INTEGER PRIMARY KEY,
        message_template TEXT
    )
    """)

    conn.commit()
    conn.close()