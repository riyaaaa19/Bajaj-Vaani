import os
import tempfile
import requests
import hashlib
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import List
from concurrent.futures import ThreadPoolExecutor

from document_parser import (
    extract_clauses_from_pdf,
    extract_clauses_from_docx,
    extract_clauses_from_eml,
)
from vector_store import initialize_vector_store, add_clauses, search_similar_clauses
from llm_reasoning import generate_response
from auth import authenticate_user, create_access_token

app = FastAPI()

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": f"Internal server error: {str(exc)}"},
    )

@app.get("/")
def root():
    return {"message": "Bajaj-Vaani is live. Use /docs for Swagger UI."}

@app.get("/api/v1/health")
def health():
    return {"status": "bajaj-vaani API is live"}

class QueryRequest(BaseModel):
    documents: str
    questions: List[str]

class QueryResponse(BaseModel):
    question: str
    answer: str

@app.post("/api/v1/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": user.username, "role": user.role})
    return {"access_token": token, "token_type": "bearer"}

def extract_and_index_clauses(blob_url: str):
    try:
        response = requests.get(blob_url, timeout=15)
        response.raise_for_status()

        suffix = blob_url.split(".")[-1].split("?")[0].lower()
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{suffix}") as tmp:
            tmp.write(response.content)
            file_path = tmp.name

        file_hash = hashlib.sha256(response.content).hexdigest()
        flag_path = f"faiss_index/{file_hash}.flag"
        if os.path.exists(flag_path):
            return

        if suffix == "pdf":
            clauses = extract_clauses_from_pdf(file_path)
        elif suffix == "docx":
            clauses = extract_clauses_from_docx(file_path)
        elif suffix == "eml":
            clauses = extract_clauses_from_eml(file_path)
        else:
            raise ValueError("Unsupported file type")

        add_clauses(clauses, source_file=blob_url)
        open(flag_path, "w").close()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"❌ Document load error: {str(e)}")

@app.post("/api/v1/bajaj-vaani/run", response_model=List[QueryResponse])
def run_query(request: QueryRequest):
    initialize_vector_store()
    extract_and_index_clauses(request.documents)

    def process(q: str):
        matched = search_similar_clauses(q, top_k=5)
        answer = generate_response(q, matched)
        return {"question": q, "answer": answer}

    with ThreadPoolExecutor() as pool:
        return list(pool.map(process, request.questions))

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port, reload=False)
