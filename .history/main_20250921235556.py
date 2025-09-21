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
import llm_reasoning  # assuming this has your LLM function

app = FastAPI(
    title="AI Chatbot - Separate Endpoints",
    version="1.0",
    description="Text chat and file uploads separated for clarity"
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
# Token store
# -------------------------
active_tokens: Dict[str, str] = {}

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
# Text-only chat endpoint
# -------------------------
@app.post("/chat", response_model=ChatResponse)
async def chat_text(
    query: str = Query(..., description="Question to ask the AI"),
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
):
    if not credentials or credentials.scheme.lower() != "bearer":
        raise HTTPException(status_code=401, detail="Missing or invalid token")
    if credentials.credentials not in active_tokens.values():
        raise HTTPException(status_code=401, detail="Invalid token")
    if not query.strip():
        raise HTTPException(status_code=400, detail="Query is empty")

    try:
        # Provide detailed answer
        answer = llm_reasoning.answer_question(
            f"You are Bajaj Vaani, an intelligent finance assistant. Answer in detail.\nQuestion:\n{query.strip()}"
        )
        logging.info(f"Q: {query}\nA: {answer}\n{'-'*60}")
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

    # Extract text from all files
    document_text = ""
    for file in files:
        document_text += extract_text_from_file(file) + "\n"

    # Combine document content with query if provided
    final_query = document_text.strip()
    if query and query.strip():
        final_query += f"\n\nUser question: {query.strip()}"

    # Ask LLM with detailed answer instruction
    try:
        answer = llm_reasoning.answer_question(
            f"You are Bajaj Vaani, an intelligent finance assistant. "
            f"Use the following document context and answer the user's question in detail.\n\n{final_query}"
        )
        logging.info(
            f"Files: {[f.filename for f in files]}\nQuery: {query}\nA: {answer}\n{'-'*60}"
        )
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
