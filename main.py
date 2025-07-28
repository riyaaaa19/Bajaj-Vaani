from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import List, Optional
from auth import authenticate_user, create_access_token, get_current_user
from document_parser import extract_clauses_from_pdf, extract_clauses_from_docx, extract_clauses_from_eml
from vector_store import search_similar_clauses, add_clauses, initialize_vector_store
from query_agent import generate_response
import tempfile
import requests
import io
import os
import logging
from contextlib import asynccontextmanager
from query_agent import get_gemini_model

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Preload Gemini model on startup
    initialize_vector_store()  # Initialize the vector store
    logging.info("✅ Startup complete, Gemini & FAISS ready")
    get_gemini_model()
    yield
    # You can add cleanup if needed later

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"],
)

class QueryRequest(BaseModel):
    documents: Optional[str]
    questions: List[str]

@app.get("/")
def root():
    return {"message": "Server is running ✅"}

@app.get("/health")
def health_check():
    return "OK", 200

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    token = create_access_token(data={"sub": user.username, "role": user.role})
    return {"access_token": token, "token_type": "bearer"}

@app.post("/run")
async def unified_run(
    documents: Optional[str] = Form(None),
    upload: Optional[UploadFile] = File(None),
    questions: List[str] = Form(...),
    user=Depends(get_current_user)
):
    try:
        if upload:
            ext = upload.filename.lower().split(".")[-1]
            content = await upload.read()
        elif documents:
            ext = documents.lower().split(".")[-1].split("?")[0]
            r = requests.get(documents)
            if r.status_code != 200:
                return {"error": "Failed to fetch document"}
            content = r.content
        else:
            return {"error": "Provide a file or document URL."}

        if ext not in {"pdf", "docx", "eml"}:
            return {"error": "Unsupported file type"}

        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{ext}") as tmp:
            tmp.write(content)
            path = tmp.name

        if ext == "pdf":
            clauses = extract_clauses_from_pdf(path)
        elif ext == "docx":
            clauses = extract_clauses_from_docx(path)
        else:
            clauses = extract_clauses_from_eml(path)

        if not clauses:
            return {"error": "No valid clauses extracted"}

        add_clauses(clauses, source_file=upload.filename if upload else documents)

        answers = []
        for question in questions:
            matched = search_similar_clauses(question)
            answer = generate_response(question, matched)
            answers.append(answer)

        return {"answers": answers}
    except Exception as e:
        logging.exception("❌ Error in /run")
        return {"error": str(e)}
