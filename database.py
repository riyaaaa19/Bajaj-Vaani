import sqlite3
from passlib.hash import bcrypt
from pathlib import Path

DB_FILE = Path("users.db")

def init_db():
    """Initialize the SQLite database and create the users table if it doesn't exist."""
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    """)
    conn.commit()
    conn.close()

def add_user(username: str, password: str) -> bool:
    """Add a new user with hashed password."""
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    hashed_pw = bcrypt.hash(password)
    try:
        cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_pw))
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        return False
    conn.close()
    return True

def verify_user(username: str, password: str) -> bool:
    """Verify a user's credentials."""
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("SELECT password FROM users WHERE username = ?", (username,))
    row = cur.fetchone()
    conn.close()
    return row is not None and bcrypt.verify(password, row[0])
