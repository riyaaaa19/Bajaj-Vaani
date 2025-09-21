# auth.py
import sqlite3, hashlib, uuid
from fastapi import HTTPException

DB = "users.db"

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT)")
    conn.commit(); conn.close()

def hash_pw(pw: str) -> str:
    return hashlib.sha256(pw.encode()).hexdigest()

def register_user(username: str, password: str):
    try:
        conn = sqlite3.connect(DB); c = conn.cursor()
        c.execute("INSERT INTO users(username,password) VALUES (?,?)", (username, hash_pw(password)))
        conn.commit(); conn.close()
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Username exists")

def verify_login(username: str, password: str) -> str:
    conn = sqlite3.connect(DB); c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, hash_pw(password)))
    user = c.fetchone(); conn.close()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return str(uuid.uuid4())  # return session token
