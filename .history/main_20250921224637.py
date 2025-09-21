from fastapi import FastAPI, HTTPException, Depends, Query, UploadFile, File
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import Optional, List, Dict
from database import init_db, add_user, verify_user
from llm_reasoning import answer_question
import logging
import uuid
from PyPDF2 import PdfReader
import docx
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="AI Chatbot with File Upload",
    version="1.0",
    description="Ask questions and get answers from uploaded documents powered by Google Gemini"
)

# -------------------------
# Enable CORS (for React frontend)
# -------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

class ChatResponse(BaseModel):
    answer: str

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
# Chat route with optional file upload
# -------------------------
@app.post("/chat", response_model=ChatResponse)
async def chat(
    query: Optional[str] = Query(None, description="Question to ask the AI"),
    files: Optional[List[UploadFile]] = File(None),
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
):
    # --- Secure token check ---
    if not credentials or not credentials.scheme or credentials.scheme.lower() != "bearer":
        raise HTTPException(status_code=401, detail="Missing or invalid token")
    
    if credentials.credentials not in active_tokens.values():
        raise HTTPException(status_code=401, detail="Invalid token")

    # --- Require at least query or files ---
    if not query and not files:
        raise HTTPException(status_code=400, detail="Provide either a query or file(s)")

    # --- Extract text from uploaded files ---
    document_text = ""
    if files:
        for file in files:
            document_text += extract_text_from_file(file) + "\n"

    # --- Prepare final prompt ---
    if query:
        final_query = f"{document_text}\n\nQuestion: {query}" if document_text else query
    else:
        final_query = document_text.strip()  # Only files, no text query

    # --- Ask LLM ---
    try:
        answer = answer_question(final_query)
        logging.info(
            f"Q: {query}\nFiles: {[f.filename for f in files or []]}\nA: {answer}\n{'-'*60}"
        )
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
