from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import List
from auth import authenticate_user, create_access_token, get_current_user
from document_parser import extract_clauses_from_pdf, extract_clauses_from_docx, extract_clauses_from_eml
from vector_store import search_similar_clauses, add_clauses
from llm_reasoning import generate_response
from query_agent import query_bajaj_vaani
from compare import compare_policies
import tempfile
import requests
import io
import os
import uvicorn
from typing import Union
from fastapi import UploadFile, File
from fastapi import Form

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Models ---
class QueryRequest(BaseModel):
    text: str

class RunRequest(BaseModel):
    documents: str  # Blob URL
    questions: List[str]

class CompareBlobRequest(BaseModel):
    url1: str
    url2: str

# --- Routes ---
@app.get("/")
def root():
    return {"message": "Server is running ✅"}

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    token = create_access_token(data={"sub": user.username, "role": user.role})
    return {"access_token": token, "token_type": "bearer"}

@app.post("/ask")
async def ask(req: QueryRequest, user=Depends(get_current_user)):
    try:
        print(f"🔐 User: {user.username} | Query: {req.text}")
        raw = query_bajaj_vaani(req.text)  # basic response
        matched = search_similar_clauses(req.text)
        explained = generate_response(req.text, matched)
        return {
            "raw_answer": raw,
            "explanation": explained
        }
    except Exception as e:
        return {"error": str(e)}

@app.post("/run")
async def run(
    documents: str = Form(None),
    upload: UploadFile = File(None),
    questions: List[str] = Form(...),
    user=Depends(get_current_user)
):
    try:
        # Step 1: Get file extension + content
        if upload:
            ext = upload.filename.lower().split(".")[-1]
            content = await upload.read()
        elif documents:
            ext = documents.lower().split(".")[-1].split("?")[0]
            r = requests.get(documents)
            if r.status_code != 200:
                return {"error": "Failed to fetch document from URL"}
            content = r.content
        else:
            return {"error": "Please provide a file or blob URL."}

        if ext not in {"pdf", "docx", "eml"}:
            return {"error": "Unsupported file type"}

        # Step 2: Save to temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{ext}") as tmp:
            tmp.write(content)
            path = tmp.name

        # Step 3: Extract clauses
        if ext == "pdf":
            clauses = extract_clauses_from_pdf(path)
        elif ext == "docx":
            clauses = extract_clauses_from_docx(path)
        elif ext == "eml":
            clauses = extract_clauses_from_eml(path)

        if not clauses:
            return {"error": "No valid clauses extracted"}

        add_clauses(clauses, source_file=upload.filename if upload else "blob_url")

        # Step 4: Generate answers
        answers = []
        for q in questions:
            matched = search_similar_clauses(q)
            answer = generate_response(q, matched)
            answers.append(answer)

        return {"answers": answers}
    except Exception as e:
        return {"error": str(e)}

@app.post("/compare-from-blob")
async def compare_from_blob(req: CompareBlobRequest, user=Depends(get_current_user)):
    try:
        r1 = requests.get(req.url1)
        r2 = requests.get(req.url2)
        if r1.status_code != 200 or r2.status_code != 200:
            return {"error": "Failed to download one or both documents."}

        file1 = io.BytesIO(r1.content)
        file2 = io.BytesIO(r2.content)

        results = compare_policies(file1, file2)

        preview = [{
            "clause_from_file1": r["clause_from_file1"][:300] + "...",
            "clause_from_file2": r["clause_from_file2"][:300] + "...",
            "similarity": round(r["similarity"], 2)
        } for r in results[:3]]

        return {
            "summary": f"{len(results)} clauses compared",
            "sample_matches": preview
        }
    except Exception as e:
        return {"error": str(e)}

# --- Run App ---
port = int(os.environ.get("PORT", 8000))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
