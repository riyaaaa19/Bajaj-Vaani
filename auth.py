from datetime import datetime, timedelta
from fastapi import HTTPException
from jose import JWTError, jwt  # use `python-jose` instead of `pyjwt`

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

VALID_USERNAME = "admin"
VALID_PASSWORD = "admin123"

def authenticate_user(username: str, password: str) -> bool:
    return username == VALID_USERNAME and password == VALID_PASSWORD

def create_token(username: str) -> str:
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": username, "exp": expire}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str) -> str:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload["sub"]
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
