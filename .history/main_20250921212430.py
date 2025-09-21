from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import List, Optional
from document_parser import parse_documents_from_url
from llm_reasoning import answer_question_with_clauses
import os
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TEAM_TOKEN = os.getenv("TEAM_TOKEN", "").strip()

app = FastAPI(
    title="Personal Document QA Assistant",
    version="1.0",
    description="Answer questions from uploaded documents using LLM + FAISS"
)

# Optional Bearer token security
security = HTTPBearer(auto_error=False)

# Log used clauses for reference/debugging
logging.basicConfig(
    filename="clause_log.txt",
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

# --- Models ---
class QueryRequest(BaseModel):
    documents: str  # URL of the document
    questions: List[str]  # List of user questions

class QueryResponse(BaseModel):
    answers: List[str]

@app.post("/api/v1/run", response_model=QueryResponse)
async def run_query(
    request: QueryRequest,
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
):
    """
    Main endpoint for querying documents.
    Authorization is optional — checked only if provided.
    """
    # Token verification if provided
    if credentials:
        if credentials.scheme.lower() != "bearer" or credentials.credentials != TEAM_TOKEN:
            raise HTTPException(status_code=401, detail="Unauthorized")

    try:
        # 1. Parse document text from URL
        full_text: str = parse_documents_from_url(request.documents)

        # 2. Process each question and collect answers
        answers: List[str] = []
        for question in request.questions:
            answer, used_clauses = answer_question_with_clauses(full_text, question)
            clean_answer = answer.strip()
            logging.info(f"Q: {question}\n{used_clauses}\n" + "-" * 60)
            answers.append(clean_answer)

        return {"answers": answers}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
