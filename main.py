from fastapi import FastAPI, Depends, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import List
from auth import authenticate_user, create_access_token, get_current_user
from document_parser import (
    extract_clauses_from_pdf,
    extract_clauses_from_docx,
    extract_clauses_from_eml,
)
from vector_store import (
    search_similar_clauses,
    add_clauses,
    initialize_vector_store,
)
from query_agent import generate_response, get_gemini_model
import tempfile, requests, os, logging
from concurrent.futures import ThreadPoolExecutor

# ✅ Setup Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# ✅ FastAPI App Initialization
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Login Endpoint (Token Auth)
@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    token = create_access_token(data={"sub": user.username, "role": user.role})
    return {"access_token": token, "token_type": "bearer"}

# ✅ Health Check
@app.get("/health")
def health_check():
    return {"status": "ok"}, 200

# ✅ Lazy Load Globals
vector_initialized = False
model_loaded = False

# ✅ Core Document-QA Endpoint
@app.post("/run")
async def run_query(
    documents: str = Form(...),
    questions: List[str] = Form(...),
    user=Depends(get_current_user)
):
    global vector_initialized, model_loaded

    try:
        # 🧠 Lazy Init FAISS
        if not vector_initialized:
            initialize_vector_store()
            vector_initialized = True

        # ⚡ Lazy Init Gemini Model
        if not model_loaded:
            get_gemini_model()
            model_loaded = True

        # 🔗 Download document from Blob URL
        ext = documents.lower().split(".")[-1].split("?")[0]
        r = requests.get(documents)
        if r.status_code != 200:
            return {"error": "Failed to fetch document"}
        content = r.content

        # 🗂 Save and parse file
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{ext}") as tmp:
            tmp.write(content)
            path = tmp.name

        if ext == "pdf":
            clauses = extract_clauses_from_pdf(path)
        elif ext == "docx":
            clauses = extract_clauses_from_docx(path)
        elif ext == "eml":
            clauses = extract_clauses_from_eml(path)
        else:
            return {"error": "Unsupported file type"}

        if not clauses:
            return {"error": "No valid clauses extracted"}

        # ➕ Add to FAISS
        add_clauses(clauses, source_file=documents)

        # ⚡ Answer each question in parallel
        def process_question(q):
            matched = search_similar_clauses(q)  # top_k = 5 internally
            answer = generate_response(q, matched)  # Gemini Flash
            return {
                "question": q,
                "answer": answer,
                "matched_clauses": matched
            }

        with ThreadPoolExecutor() as executor:
            results = list(executor.map(process_question, questions))

        return {"answers": results}

    except Exception as e:
        logging.exception("❌ Error during /run")
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
