from fastapi import FastAPI, UploadFile, File, Form, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from fastapi.security import OAuth2PasswordRequestForm
from auth import authenticate_user, create_access_token, get_current_user, User
from query_agent import query_bajaj_vaani
from document_parser import (
    extract_clauses_from_pdf,
    extract_clauses_from_docx,
    extract_clauses_from_eml
)
from vector_store import search_similar_clauses, add_clauses
from llm_reasoning import generate_response
from compare import compare_policies
from datetime import timedelta
import tempfile
import io
import requests


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    text: str

class UploadAndAskRequest(BaseModel):
    documents: str  # Blob or file URL
    questions: List[str]

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": user.username, "role": user.role})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/secure-endpoint")
def secure(user=Depends(get_current_user)):
    return {"message": f"Welcome {user.username}", "role": user.role}

@app.post("/query")
async def query(req: QueryRequest):
    user = get_current_user()
    print(f"🔐 Accessed by: {user.username}")
    try:
        user_input = req.text
        print(f"🟢 Query: {user_input}")
        answer = query_bajaj_vaani(user_input)
        return {"response": answer}
    except Exception as e:
        print(f"❌ /query error: {e}")
        return {"error": str(e)}

@app.post("/reasoning")
async def reasoning(req: QueryRequest):
    try:
        user_input = req.text
        matched = search_similar_clauses(user_input)
        result = generate_response(user_input, matched)
        return {"response": result}
    except Exception as e:
        print(f"❌ /reasoning error: {e}")
        return {"error": str(e)}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        ext = file.filename.lower().split(".")[-1]
        supported_formats = {"pdf", "docx", "eml"}

        if ext not in supported_formats:
            return {"error": "Unsupported file format"}

        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{ext}") as tmp:
            tmp.write(await file.read())
            tmp_path = tmp.name

        if ext == "pdf":
            clauses = extract_clauses_from_pdf(tmp_path)
        elif ext == "docx":
            clauses = extract_clauses_from_docx(tmp_path)
        elif ext == "eml":
            clauses = extract_clauses_from_eml(tmp_path)
        else:
            return {"error": "Unsupported file format"}

        if not clauses:
            return {"error": "No valid clauses found."}

        add_clauses(clauses, source_file=file.filename)

        return {
            "message": f"✅ {len(clauses)} clauses indexed from {file.filename}",
            "clauses": clauses[:3]
        }

    except Exception as e:
        print(f"❌ /upload error: {e}")
        return {"error": str(e)}

@app.post("/compare")
async def compare_documents(
    file1: UploadFile = File(...),
    file2: UploadFile = File(...),
    summary: Optional[bool] = Form(False),
    top_k: Optional[int] = Form(None)
):
    try:
        content1 = await file1.read()
        content2 = await file2.read()

        results = compare_policies(
            io.BytesIO(content1),
            io.BytesIO(content2),
            top_k=top_k or 1
        )

        if summary:
            preview = []
            for match in results[:3]:
                clause1 = match.get("clause_from_file1", "")
                clause2 = match.get("clause_from_file2", "")
                similarity = match.get("similarity", 0.0)

                preview.append({
                    "clause_from_file1": (clause1[:300] + "...") if len(clause1) > 300 else clause1,
                    "clause_from_file2": (clause2[:300] + "...") if len(clause2) > 300 else clause2,
                    "similarity": round(similarity, 2)
                })

            return {
                "summary": f"{len(results)} clauses compared",
                "sample_matches": preview
            }

        return {"comparison": results}
    except Exception as e:
        print(f"❌ /compare error: {e}")
        return {"error": str(e)}


@app.post("/upload-and-ask")
async def upload_and_ask(
    file: UploadFile = File(...),
    questions: List[str] = Form(...)
):
    try:
        ext = file.filename.lower().split(".")[-1]
        supported_formats = {"pdf", "docx", "eml"}
        if ext not in supported_formats:
            return {"error": "Unsupported file format"}

        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{ext}") as tmp:
            tmp.write(await file.read())
            tmp_path = tmp.name

        # Extract clauses
        if ext == "pdf":
            clauses = extract_clauses_from_pdf(tmp_path)
        elif ext == "docx":
            clauses = extract_clauses_from_docx(tmp_path)
        elif ext == "eml":
            clauses = extract_clauses_from_eml(tmp_path)
        else:
            return {"error": "Unsupported file format"}

        if not clauses:
            return {"error": "No valid clauses found in document."}

        # Add clauses to FAISS
        add_clauses(clauses, source_file=file.filename)

        # Answer questions
        answers = []
        for q in questions:
            matched = search_similar_clauses(q)
            result = generate_response(q, matched)
            answers.append(result)

        return {"answers": answers}

    except Exception as e:
        print(f"❌ /upload-and-ask error: {e}")
        return {"error": str(e)}
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8000))
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=port)


