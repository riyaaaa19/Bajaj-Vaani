import os
from datetime import datetime, timedelta
from typing import Optional

from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

# 🔒 Load environment variables
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("TOKEN_EXPIRY", "60"))
AUTH_ENABLED = os.getenv("AUTH_ENABLED", "true").lower() == "true"

# 🔐 Password Hashing Context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 📲 OAuth2 Bearer Setup
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# 🧑‍💻 Dummy User DB (for HackRx)
fake_users_db = {
    "judge": {
        "username": "judge",
        "full_name": "Hackathon Judge",
        "hashed_password": "$2b$12$RjGJN1TegbzUyvKqJzNDkOvRgiYcOmNfIuSW93CIDGABtZCKdB1fm",  # password: demo123
        "role": "admin"
    }
}

# 🧑‍🎓 User Model
class User:
    def __init__(self, username: str, role: str):
        self.username = username
        self.role = role

# ✅ Verify password using bcrypt
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# ✅ Authenticate against the fake DB
def authenticate_user(username: str, password: str) -> Optional[User]:
    user = fake_users_db.get(username)
    if not user or not verify_password(password, user["hashed_password"]):
        return None
    return User(username=user["username"], role=user["role"])

# ✅ Generate signed JWT access token
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# ✅ Get current user from token or anonymous (if AUTH_ENABLED = false)
def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    if not AUTH_ENABLED:
        return User(username="anonymous", role="guest")

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing token",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        role = payload.get("role", "user")
        if not username:
            raise credentials_exception
        return User(username=username, role=role)
    except JWTError:
        raise credentials_exception
