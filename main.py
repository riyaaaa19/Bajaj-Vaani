from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import List
from document_parser import parse_documents_from_url
from llm_reasoning import answer_question_with_clauses
import os
from dotenv import load_dotenv

load_dotenv()
TEAM_TOKEN = os.getenv("TEAM_TOKEN")

app = FastAPI()

security = HTTPBearer()

class QueryRequest(BaseModel):
    documents: str
    questions: List[str]

class QueryResponse(BaseModel):
    answers: List[str]

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
            answer, _ = answer_question_with_clauses(full_text, question)
            answers.append(answer)  # Only store clean answer
        return {"answers": answers}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
