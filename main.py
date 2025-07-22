from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import tempfile
from query_agent import query_bajaj_vaani
from document_parser import extract_clauses_from_pdf
from vector_store import search_similar_clauses, add_clauses
from llm_reasoning import generate_response

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

@app.post("/query")
async def query(req: QueryRequest):
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
async def upload_pdf(file: UploadFile = File(...)):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(await file.read())
            path = tmp.name

        clauses = extract_clauses_from_pdf(path)  # ✅ Corrected function
        add_clauses(clauses)

        return {
            "message": f"✅ {len(clauses)} clauses indexed",
            "clauses": clauses
        }
    except Exception as e:
        print(f"❌ /upload error: {e}")
        return {"error": str(e)}
