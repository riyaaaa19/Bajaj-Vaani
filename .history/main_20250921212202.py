from fastapi import FastAPI, HTTPException, Depends, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import List, Optional
from dotenv import load_dotenv
import logging, os

from document_parser import parse_documents_from_url
from llm_reasoning import answer_question_with_clauses
from auth import init_db, register_user, verify_login

load_dotenv()
init_db()

app = FastAPI(title="HackRx Clause-Based QA", version="2.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"]
)

security = HTTPBearer(auto_error=False)

logging.basicConfig(filename="clause_log.txt", level=logging.INFO, format="%(asctime)s - %(message)s")

# Models
class QueryRequest(BaseModel):
    documents: str
    questions: List[str]

class QueryResponse(BaseModel):
    answers: List[str]

class AuthRequest(BaseModel):
    username: str
    password: str

# -------- AUTH --------
@app.post("/register")
async def register(req: AuthRequest):
    register_user(req.username, req.password)
    return {"message": "Registered"}

@app.post("/login")
async def login(req: AuthRequest):
    token = verify_login(req.username, req.password)
    return {"token": token}

# -------- FILE UPLOAD --------
@app.post("/upload")
async def upload(files: List[UploadFile] = File(...)):
    os.makedirs("uploads", exist_ok=True)
    saved = []
    for f in files:
        path = os.path.join("uploads", f.filename)
        with open(path, "wb") as buf:
            buf.write(await f.read())
        saved.append(f.filename)
    return {"uploaded": saved}

# -------- QUICK CHAT --------
@app.post("/chat")
async def chat(query: str):
    # Minimal delay quick response
    return {"response": f"Echo: {query}"}

# -------- EXISTING QA ENDPOINT --------
@app.post("/api/v1/hackrx/run", response_model=QueryResponse)
async def run_query(request: QueryRequest, credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)):
    if credentials and credentials.scheme.lower() == "bearer":
        pass  # optional auth removed; rely on login for UI

    try:
        text = parse_documents_from_url(request.documents)
        answers = []
        for q in request.questions:
            ans, used = answer_question_with_clauses(text, q)
            logging.info(f"Q:{q}\n{used}\n{'-'*40}")
            answers.append(ans.strip())
        return {"answers": answers}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
