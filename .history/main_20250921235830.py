from fastapi import FastAPI, HTTPException, Depends, Query, UploadFile, File, Form
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import Optional, List, Dict
from database import init_db, add_user, verify_user
import logging
import uuid
from PyPDF2 import PdfReader
import docx
from fastapi.middleware.cors import CORSMiddleware
import llm_reasoning

app = FastAPI(
    title="AI Chatbot - Document Session Memory",
    version="1.1",
    description="Chatbot with persistent document context per session"
)

# -------------------------
# Enable CORS
# -------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------
# Token & Document Context store
# -------------------------
active_tokens: Dict[str, str] = {}
document_context: Dict[str, str] = {}  # key=username, value=combined document text

# -------------------------
# Initialize DB
# -------------------------
@app.on_event("startup")
def startup_event():
    init_db()

# -------------------------
# Security
# -------------------------
security = HTTPBearer(auto_error=False)

# -------------------------
# Logging
# -------------------------
logging.basicConfig(
    filename="chat_log.txt",
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

# -------------------------
# Models
# -------------------------
class User(BaseModel):
    username: str
    password: str

class ChatResponse(BaseModel):
    answer: str

# -------------------------
# Helper function
# -------------------------
def extract_text_from_file(file: UploadFile) -> str:
    filename = file.filename or ""
    lower_fname = filename.lower()
    if lower_fname.endswith(".pdf"):
        reader = PdfReader(file.file)
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    elif lower_fname.endswith(".docx"):
        doc = docx.Document(file.file)
        return "\n".join(p.text for p in doc.paragraphs)
    elif lower_fname.endswith(".txt"):
        return file.file.read().decode("utf-8")
    else:
        raise HTTPException(status_code=400, detail=f"Unsupported file type: {filename}")

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
        token = str(uuid.uuid4())
        active_tokens[user.username] = token
        return {"access_token": token, "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="Invalid credentials.")

# -------------------------
# Chat endpoint (text-only or with persistent document)
# -------------------------
@app.post("/chat", response_model=ChatResponse)
async def chat_text(
    query: str = Query(..., description="Question to ask the AI"),
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
):
    # Token validation
    if not credentials or credentials.scheme.lower() != "bearer":
        raise HTTPException(status_code=401, detail="Missing or invalid token")
    if credentials.credentials not in active_tokens.values():
        raise HTTPException(status_code=401, detail="Invalid token")
    if not query.strip():
        raise HTTPException(status_code=400, detail="Query is empty")

    # Find the username from token
    username = next((u for u, t in active_tokens.items() if t == credentials.credentials), None)

    # Retrieve previous document context if exists
    doc_context = document_context.get(username, "")

    # Combine document context with user query
    final_query = doc_context.strip()
    if final_query:
        final_query += f"\n\nUser question: {query.strip()}"
    else:
        final_query = query.strip()

    try:
        # Ask LLM with detailed answer instruction
        answer = llm_reasoning.answer_question(
            f"You are Bajaj Vaani, an intelligent finance assistant. "
            f"Use the following context to answer the user's question in detail.\n\n{final_query}"
        )
        logging.info(f"User: {username}\nQ: {query}\nA: {answer}\n{'-'*60}")
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# -------------------------
# File upload + optional query endpoint
# -------------------------
@app.post("/upload", response_model=ChatResponse)
async def chat_file(
    files: List[UploadFile] = File(..., description="Upload file(s) to provide context"),
    query: Optional[str] = Form(None, description="Optional question to ask after uploading files"),
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
):
    if not credentials or credentials.scheme.lower() != "bearer":
        raise HTTPException(status_code=401, detail="Missing or invalid token")
    if credentials.credentials not in active_tokens.values():
        raise HTTPException(status_code=401, detail="Invalid token")
    if not files:
        raise HTTPException(status_code=400, detail="No files uploaded")

    username = next((u for u, t in active_tokens.items() if t == credentials.credentials), None)

    # Extract text from all files
    document_text = ""
    for file in files:
        document_text += extract_text_from_file(file) + "\n"

    # Save or append to user's document context
    if username:
        if username in document_context:
            document_context[username] += "\n" + document_text
        else:
            document_context[username] = document_text

    # Combine with query if provided
    final_query = document_context.get(username, "").strip()
    if query and query.strip():
        final_query += f"\n\nUser question: {query.strip()}"

    try:
        answer = llm_reasoning.answer_question(
            f"You are Bajaj Vaani, an intelligent finance assistant. "
            f"Use the following context to answer the user's question in detail.\n\n{final_query}"
        )
        logging.info(f"User: {username}\nFiles: {[f.filename for f in files]}\nQuery: {query}\nA: {answer}\n{'-'*60}")
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
