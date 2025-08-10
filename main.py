# main.py
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import List, Optional
from document_parser import parse_documents_from_url
from llm_reasoning import answer_question_with_clauses
import os
import logging
from dotenv import load_dotenv

# Load env vars
load_dotenv()
TEAM_TOKEN = os.getenv("TEAM_TOKEN", "").strip()

app = FastAPI(
    title="HackRx Clause-Based QA",
    version="1.0",
    description="Answer insurance-related questions from uploaded documents using LLM + FAISS"
)

# Optional Auth
security = HTTPBearer(auto_error=False)

# Logging for used clauses
logging.basicConfig(
    filename="clause_log.txt",
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

# Models
class QueryRequest(BaseModel):
    documents: str
    questions: List[str]

class QueryResponse(BaseModel):
    answers: List[str]

@app.post("/api/v1/hackrx/run", response_model=QueryResponse)
async def run_query(
    request: QueryRequest,
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
):
    """
    Main HackRx endpoint.
    Authorization is optional — token check runs only if provided.
    """
    if credentials:
        if credentials.scheme.lower() != "bearer" or credentials.credentials != TEAM_TOKEN:
            raise HTTPException(status_code=401, detail="Unauthorized")

    try:
        # Step 1: Parse document text
        full_text = parse_documents_from_url(request.documents)

        # Step 2: Process each question
        answers = []
        for question in request.questions:
            answer, used_clauses = answer_question_with_clauses(full_text, question)
            clean_answer = answer.strip()
            logging.info(f"Q: {question}\n{used_clauses}\n" + "-" * 60)
            answers.append(clean_answer)

        return {"answers": answers}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
