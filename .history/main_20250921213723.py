# main.py
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import Optional
from llm_reasoning import answer_question_direct
from database import init_db, add_user, verify_user
import logging
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TEAM_TOKEN = os.getenv("TEAM_TOKEN", "").strip()

# Initialize FastAPI
app = FastAPI(
    title="Personal Document QA Assistant",
    version="1.0",
    description="Answer questions from uploaded documents using LLM"
)

# Database init
@app.on_event("startup")
def startup():
    init_db()

# Optional Bearer token security
security = HTTPBearer(auto_error=False)

# Logging
logging.basicConfig(
    filename="clause_log.txt",
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

# Models
class User(BaseModel):
    username: str
    password: str

class ChatRequest(BaseModel):
    document_text: str
    query: str

# Routes
@app.post("/register")
async def register(user: User):
    if not add_user(user.username, user.password):
        raise HTTPException(status_code=400, detail="Username already exists.")
    return {"message": "User registered successfully."}

@app.post("/login")
async def login(user: User):
    if verify_user(user.username, user.password):
        return {"message": "Login successful."}
    raise HTTPException(status_code=401, detail="Invalid credentials.")

@app.post("/chat")
async def chat(
    request: ChatRequest,
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
):
    if credentials:
        if credentials.scheme.lower() != "bearer" or credentials.credentials != TEAM_TOKEN:
            raise HTTPException(status_code=401, detail="Unauthorized")

    try:
        answer = answer_question_direct(request.document_text, request.query)
        logging.info(f"Q: {request.query}\nAnswer: {answer}\n" + "-"*60)
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
