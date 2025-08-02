from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from jose import JWTError, jwt
from document_parser import parse_documents_from_url
from llm_reasoning import ask_questions_with_reasoning
import os

SECRET_KEY = "hackrx"
ALGORITHM = "HS256"

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class HackRXRequest(BaseModel):
    documents: str
    questions: List[str]

def get_current_user_optional(authorization: Optional[str] = Header(None)):
    if not authorization:
        return None
    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            return None
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username:
            return {"username": username}
    except (JWTError, ValueError):
        pass
    return None

@app.post("/hackrx/run")
def run_query(request: HackRXRequest, user: Optional[dict] = Depends(get_current_user_optional)):
    docs = parse_documents_from_url(request.documents)
    answers = []
    for question in request.questions:
        answer, _clauses = ask_questions_with_reasoning(docs, question)
        answers.append(answer)
    return {"answers": answers}
