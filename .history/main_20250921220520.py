from fastapi import FastAPI, HTTPException, Depends, Query, UploadFile, File, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import Optional, List, Dict
from database import init_db, add_user, verify_user
from llm_reasoning import answer_question
import logging
import uuid
from PyPDF2 import PdfReader
import docx
import os

app = FastAPI(
    title="AI Chatbot with File Upload",
    version="1.0",
    description="Ask questions and get answers from uploaded documents powered by Google Gemini"
)

# -------------------------
# Serve frontend static files
# -------------------------
frontend_dir = os.path.join(os.path.dirname(__file__), "frontend")
app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="frontend")

# -------------------------
# In-memory token store
# -------------------------
active_tokens: Dict[str, str] = {}

# -------------------------
# Initialize database
# -------------------------
@app.on_event("startup")
def startup():
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

# -------------------------
# Helper functions
# -------------------------
def extract_text_from_file(file: UploadFile) -> str:
    """Extract text from PDF, DOCX, or TXT files."""
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
# User API
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
        response = RedirectResponse(url="/chat.html")
        response.set_cookie(key="access_token", value=token)
        return response
    raise HTTPException(status_code=401, detail="Invalid credentials.")

# -------------------------
# Chat API
# -------------------------
@app.post("/chat")
async def chat(
    query: str = Form(...),
    files: Optional[List[UploadFile]] = File(None),
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
):
    # Token validation (from header or cookie)
    token = credentials.credentials if credentials else None
    if not token:
        raise HTTPException(status_code=401, detail="Missing token")

    if token not in active_tokens.values():
        raise HTTPException(status_code=401, detail="Invalid token")

    if not query.strip():
        raise HTTPException(status_code=400, detail="Query is empty")

    # Extract text from uploaded files
    document_text = ""
    if files:
        for file in files:
            document_text += extract_text_from_file(file) + "\n"

    # Prepare final query
    final_query = f"{document_text}\n\nQuestion: {query}" if document_text else query

    # Ask LLM
    try:
        answer = answer_question(final_query)
        logging.info(f"Q: {query}\nFiles: {[f.filename for f in files or []]}\nA: {answer}\n{'-'*60}")
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
