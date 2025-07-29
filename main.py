import os
import tempfile
import requests
from fastapi import FastAPI, Request, UploadFile, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import List
from concurrent.futures import ThreadPoolExecutor

from document_parser import (
    extract_clauses_from_pdf,
    extract_clauses_from_docx,
    extract_clauses_from_eml
)
from vector_store import initialize_vector_store, add_clauses, search_similar_clauses
from llm_reasoning import generate_response
from auth import authenticate_user, create_access_token

app = FastAPI()

# ----------------------
# 🔄 Data Models
# ----------------------
class QueryRequest(BaseModel):
    documents: str  # Blob URL
    questions: List[str]

# ----------------------
# 🔧 Startup
# ----------------------
initialize_vector_store()

# ----------------------
# 📥 Download & Parse
# ----------------------
def download_blob(blob_url: str) -> str:
    response = requests.get(blob_url)
    suffix = ".pdf" if ".pdf" in blob_url else (".docx" if ".docx" in blob_url else ".eml")
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    temp_file.write(response.content)
    temp_file.close()
    return temp_file.name

# ----------------------
# 🤖 Process Query
# ----------------------
def process_question(query: str, clauses: List[str]) -> dict:
    trimmed = [clause.strip()[:500] for clause in clauses if clause.strip()]
    query_lower = query.lower()

    # ✅ Prefer clause-based if it matches all key words
    for clause in trimmed:
        if all(word in clause.lower() for word in query_lower.split()):
            return {
                "question": query,
                "answer": clause.strip(),
                "source": "clause",
                "matched_clauses": clauses
            }

    # 🤖 Use Gemini with strict summarization prompt
    answer = generate_response(query, clauses)
    return {
        "question": query,
        "answer": answer,
        "source": "gemini",
        "matched_clauses": clauses
    }
    
# ----------------------
# 🔐 Login Endpoint (JWT)
# ----------------------
@app.post("/api/v1/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )
    token = create_access_token({"sub": user.username, "role": user.role})
    return {"access_token": token, "token_type": "bearer"}


# ----------------------
# 🚀 Main API Endpoint
# ----------------------
@app.post("/api/v1/bajaj-vaani/run")
async def run_query(req: QueryRequest):
    file_path = download_blob(req.documents)

    if file_path.endswith(".pdf"):
        clauses = extract_clauses_from_pdf(file_path)
    elif file_path.endswith(".docx"):
        clauses = extract_clauses_from_docx(file_path)
    elif file_path.endswith(".eml"):
        clauses = extract_clauses_from_eml(file_path)
    else:
        return {"error": "Unsupported file type"}

    add_clauses(clauses, source_file=os.path.basename(file_path))

    # 🔍 Parallel question processing
    with ThreadPoolExecutor() as executor:
        results = list(executor.map(lambda q: process_question(q, search_similar_clauses(q)), req.questions))

    return {"answers": results}


# ----------------------
# 🩺 Health Check
# ----------------------
@app.get("/api/v1/health")
def health_check():
    return {"status": "ok", "message": "Bajaj Vaani is healthy"}
