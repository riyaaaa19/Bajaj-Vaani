from fastapi import FastAPI, HTTPException, Depends, Query, UploadFile, File
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import Optional, Dict, List
from llm_reasoning import answer_question
from database import init_db, add_user, verify_user
import logging
import uuid
import io
from PyPDF2 import PdfReader
import docx

app = FastAPI(
    title="AI Chatbot with File Upload",
    version="1.0",
    description="Ask questions and get answers from uploaded documents powered by Google Gemini"
)

# In-memory token store
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
# Helper functions
# -------------------------
def extract_text_from_file(file: UploadFile) -> str:
    """Extract text from PDF, DOCX, or TXT files."""
    if file.filename.lower().endswith(".pdf"):
        reader = PdfReader(file.file)
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    elif file.filename.lower().endswith(".docx"):
        doc = docx.Document(file.file)
        return "\n".join(p.text for p in doc.paragraphs)
    elif file.filename.lower().endswith(".txt"):
        return file.file.read().decode("utf-8")
    else:
        raise HTTPException(status_code=400, detail=f"Unsupported file type: {file.filename}")

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
# Chat route with file upload
# -------------------------
@app.post("/chat", response_model=ChatResponse)
async def chat(
    query: str = Query(..., description="Question to ask the AI"),
    files: Optional[List[UploadFile]] = File(None),
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
):
    # --- Secure token check ---
    if not credentials or not credentials.scheme or credentials.scheme.lower() != "bearer":
        raise HTTPException(status_code=401, detail="Missing or invalid token")
    
    if credentials.credentials not in active_tokens.values():
        raise HTTPException(status_code=401, detail="Invalid token")

    if not query.strip():
        raise HTTPException(status_code=400, detail="Query is empty")

    # --- Extract text from uploaded files ---
    document_text = ""
    if files:
        for file in files:
            document_text += extract_text_from_file(file) + "\n"

    # --- Prepare final prompt ---
    final_query = f"{document_text}\n\nQuestion: {query}" if document_text else query

    # --- Ask LLM ---
    try:
        answer = answer_question(final_query)
        logging.info(
            f"Q: {query}\nFiles: {[f.filename for f in files or []]}\nA: {answer}\n{'-'*60}"
        )
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
