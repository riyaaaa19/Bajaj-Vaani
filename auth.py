import os
from datetime import datetime, timedelta
from fastapi import HTTPException
from jose import JWTError, jwt
from dotenv import load_dotenv

load_dotenv()

# Load from .env securely
SECRET_KEY = os.getenv("SECRET_KEY", "fallback_dev_secret")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# Dummy user for demo — use database in production
VALID_USERNAME = os.getenv("VALID_USERNAME", "admin")
VALID_PASSWORD = os.getenv("VALID_PASSWORD", "admin123")

def authenticate_user(username: str, password: str) -> bool:
    return username == VALID_USERNAME and password == VALID_PASSWORD

def create_token(username: str) -> str:
    to_encode = {
        "sub": username,
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    }
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str) -> str:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if not username:
            raise HTTPException(status_code=401, detail="Invalid token payload")
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
