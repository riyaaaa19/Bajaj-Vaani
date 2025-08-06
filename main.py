from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import List
from document_parser import parse_documents_from_url
from llm_reasoning import answer_question_with_clauses
import os
import logging
from dotenv import load_dotenv

# Load environment variable
load_dotenv()
TEAM_TOKEN = os.getenv("TEAM_TOKEN")

# FastAPI app with security scheme metadata for Swagger UI
app = FastAPI(
    title="HackRx Clause-Based QA",
    version="1.0",
    description="Answer questions from uploaded documents using LLM + FAISS",
    openapi_tags=[{
        "name": "default",
        "description": "Run queries on documents"
    }]
)

# Auth scheme - REQUIRED for Authorize button to show
security = HTTPBearer(auto_error=False)

# Logging
logging.basicConfig(
    filename="clause_log.txt",
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

# Request and response models
class QueryRequest(BaseModel):
    documents: str
    questions: List[str]

class QueryResponse(BaseModel):
    answers: List[str]

# Auth-protected route
@app.post("/api/v1/hackrx/run", response_model=QueryResponse)
async def run_query(
    request: QueryRequest,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    if not credentials or credentials.scheme.lower() != "bearer" or credentials.credentials != TEAM_TOKEN:
        raise HTTPException(status_code=401, detail="Unauthorized")

    try:
        full_text = parse_documents_from_url(request.documents)
        answers = []

        for question in request.questions:
            answer, used_clauses = answer_question_with_clauses(full_text, question)
            logging.info(f"Q: {question}\n{used_clauses}\n" + "-" * 60)
            answers.append(answer)

        return {"answers": [a.strip().split("\n\n")[0] for a in answers]}


    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
