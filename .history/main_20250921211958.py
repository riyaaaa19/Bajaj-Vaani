from fastapi import FastAPI, HTTPException, Depends, UploadFile, File
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import sqlite3, hashlib, uuid, os, logging
from dotenv import load_dotenv
from document_parser import parse_documents_from_url
from llm_reasoning import answer_question_with_clauses

# --- Load environment ---
load_dotenv()
TEAM_TOKEN = os.getenv("TEAM_TOKEN", "").strip()

# --- App setup ---
app = FastAPI(title="HackRx Clause-Based QA", version="1.1")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"]
)

security = HTTPBearer(auto_error=False)

# --- Logging ---
logging.basicConfig(filename="clause_log.txt", level=logging.INFO, format="%(asctime)s - %(message)s")

# --- Database for Auth ---
DB = "users.db"
if not os.path.exists(DB):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("CREATE TABLE users(id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT)")
    conn.commit(); conn.close()

def hash_pw(pw: str) -> str: return hashlib.sha256(pw.encode()).hexdigest()

# --- Models ---
class QueryRequest(BaseModel):
    documents: str
    questions: List[str]

class QueryResponse(BaseModel):
    answers: List[str]

class AuthRequest(BaseModel):
    username: str
    password: str

# --- Auth Endpoints ---
@app.post("/register")
async def register(req: AuthRequest):
    try:
        conn = sqlite3.connect(DB); c = conn.cursor()
        c.execute("INSERT INTO users(username,password) VALUES (?,?)", (req.username, hash_pw(req.password)))
        conn.commit(); conn.close()
        return {"message": "User registered"}
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Username exists")

@app.post("/login")
async def login(req: AuthRequest):
    conn = sqlite3.connect(DB); c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (req.username, hash_pw(req.password)))
    user = c.fetchone(); conn.close()
    if not user: raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"token": str(uuid.uuid4())}

# --- Upload Multiple Files ---
@app.post("/upload")
async def upload(files: List[UploadFile] = File(...)):
    os.makedirs("uploads", exist_ok=True)
    names = []
    for f in files:
        path = os.path.join("uploads", f.filename)
        with open(path, "wb") as buffer:
            buffer.write(await f.read())
        names.append(f.filename)
    return {"uploaded": names}

# --- Chat Endpoint ---
@app.post("/chat")
async def chat(query: str):
    # quick echo behaviour (replace with your fast inference)
    return {"response": f"Echo: {query}"}

# --- Existing QA Endpoint ---
@app.post("/api/v1/hackrx/run", response_model=QueryResponse)
async def run_query(request: QueryRequest, credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)):
    if credentials:
        if credentials.scheme.lower() != "bearer" or credentials.credentials != TEAM_TOKEN:
            raise HTTPException(status_code=401, detail="Unauthorized")
    try:
        full_text = parse_documents_from_url(request.documents)
        answers = []
        for question in request.questions:
            answer, used_clauses = answer_question_with_clauses(full_text, question)
            logging.info(f"Q:{question}\n{used_clauses}\n" + "-"*50)
            answers.append(answer.strip())
        return {"answers": answers}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
