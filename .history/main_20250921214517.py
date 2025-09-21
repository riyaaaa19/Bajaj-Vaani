# main.py
from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import Optional, Dict
from llm_reasoning import answer_question
from database import init_db, add_user, verify_user
import logging
import uuid

app = FastAPI(
    title="AI Chatbot with Login",
    version="1.0",
    description="Ask questions and get answers powered by Google Gemini"
)

# In-memory token store (username -> token)
active_tokens: Dict[str, str] = {}

# Initialize database
@app.on_event("startup")
def startup():
    init_db()

# Security
security = HTTPBearer(auto_error=False)

# Logging
logging.basicConfig(
    filename="chat_log.txt",
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

# Models
class User(BaseModel):
    username: str
    password: str

class ChatResponse(BaseModel):
    answer: str

# -------------------------
# User routes
# -------------------------
@app.post("/register")
async def register(user: User):
    if not add_user(user.username, user.password):
        raise HTTPException(status_code=400, detail="Username already exists.")
    return {"message": "User registered successfully."}

@app.post("/login")
async def login(user: User):
    if verify_user(user.username, user.password):
        # Generate a new token
        token = str(uuid.uuid4())
        active_tokens[user.username] = token
        return {"access_token": token, "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="Invalid credentials.")

# -------------------------
# Chat route
# -------------------------
@app.post("/chat", response_model=ChatResponse)
async def chat(
    query: str = Query(..., description="Question to ask the AI"),
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
):
    if not credentials or credentials.scheme.lower() != "bearer":
        raise HTTPException(status_code=401, detail="Missing or invalid token")

    # Check if token is valid
    if credentials.credentials not in active_tokens.values():
        raise HTTPException(status_code=401, detail="Invalid token")

    if not query.strip():
        raise HTTPException(status_code=400, detail="Query is empty")

    try:
        answer = answer_question(query)
        logging.info(f"Q: {query}\nA: {answer}\n{'-'*60}")
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
