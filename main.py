from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from auth import SECRET_KEY, ALGORITHM
from jose import jwt
import time
from llm_reasoning import get_answer_from_llm
from document_parser import parse_documents_from_url
from vector_store import retrieve_clauses

app = FastAPI()

# Allow CORS (adjust for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dummy user for /login auth
FAKE_USER_DB = {
    "admin": "admin123"
}

# ==== Schemas ====

class LoginRequest(BaseModel):
    username: str
    password: str

class QueryRequest(BaseModel):
    documents: str
    questions: list[str]

class AnswerResponse(BaseModel):
    answers: list[str]

# ==== Auth Routes ====

@app.post("/login")
def login(data: LoginRequest):
    if FAKE_USER_DB.get(data.username) != data.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    payload = {
        "sub": data.username,
        "iat": int(time.time()),
        "exp": int(time.time()) + 3600
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}

# ==== Core Route ====

@app.post("/api/v1/bajaj-vaani/run", response_model=AnswerResponse)
def run_query(payload: QueryRequest):
    try:
        # Parse + embed + index
        parsed_clauses = parse_documents_from_url(payload.documents)

        # Retrieve relevant clauses
        relevant_chunks = retrieve_clauses(parsed_clauses, payload.questions)

        # LLM reasoning
        final_answers = get_answer_from_llm(relevant_chunks, payload.questions)

        return {"answers": final_answers}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Health check
@app.get("/")
def health():
    return {"status": "running"}

if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port, reload=False)