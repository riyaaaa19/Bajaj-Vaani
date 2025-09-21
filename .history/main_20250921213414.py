# main.py
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import List, Optional
from llm_reasoning import answer_question_with_clauses
from database import init_db, add_user, verify_user
import logging
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TEAM_TOKEN = os.getenv("TEAM_TOKEN", "").strip()

# Initialize FastAPI app
app = FastAPI(
    title="Personal Document QA Assistant",
    version="1.0",
    description="Answer questions from uploaded documents using LLM + FAISS"
)

# Initialize database at startup
@app.on_event("startup")
def startup():
    init_db()

# Optional token security
security = HTTPBearer(auto_error=False)

# Logging setup
logging.basicConfig(
    filename="clause_log.txt",
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

# Models
class QueryRequest(BaseModel):
    documents: str
    questions: List[str]

class QueryResponse(BaseModel):
    answers: List[str]

class User(BaseModel):
    username: str
    password: str

class ChatRequest(BaseModel):
    document_text: str
    query: str

# Routes
@app.post("/register")
async def register(user: User):
    """Register a new user."""
    if not add_user(user.username, user.password):
        raise HTTPException(status_code=400, detail="Username already exists.")
    return {"message": "User registered successfully."}

@app.post("/login")
async def login(user: User):
    """Login a user."""
    if verify_user(user.username, user.password):
        return {"message": "Login successful."}
    raise HTTPException(status_code=401, detail="Invalid credentials.")

@app.post("/api/v1/run", response_model=QueryResponse)
async def run_query(
    request: QueryRequest,
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
):
    """Endpoint for querying documents (multiple questions)."""
    if credentials:
        if credentials.scheme.lower() != "bearer" or credentials.credentials != TEAM_TOKEN:
            raise HTTPException(status_code=401, detail="Unauthorized")

    try:
        full_text = request.documents
        answers = []
        for question in request.questions:
            answer, used_clauses = answer_question_with_clauses(full_text, question)
            answers.append(answer.strip())
            logging.info(f"Q: {question}\n{used_clauses}\n" + "-" * 60)
        return {"answers": answers}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat")
async def chat(
    request: ChatRequest,
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
):
    """
    Chat endpoint where user provides document text and a single question.
    """
    if credentials:
        if credentials.scheme.lower() != "bearer" or credentials.credentials != TEAM_TOKEN:
            raise HTTPException(status_code=401, detail="Unauthorized")

    try:
        full_text = request.document_text
        answer, used_clauses = answer_question_with_clauses(full_text, request.query)
        logging.info(f"Q: {request.query}\n{used_clauses}\n" + "-" * 60)
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
