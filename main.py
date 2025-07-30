import logging
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from document_parser import parse_documents_from_url
from llm_reasoning import answer_question
from auth import authenticate_user, create_token, verify_token

app = FastAPI(title="Bajaj Vaani API")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
logging.basicConfig(level=logging.INFO)

class RunQueryRequest(BaseModel):
    documents: str
    questions: list[str]

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if authenticate_user(form_data.username, form_data.password):
        token = create_token(form_data.username)
        return {"access_token": token, "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="Invalid credentials")

@app.post("/api/v1/bajaj-vaani/run")
def run_query(
    payload: RunQueryRequest,
    token: str = Depends(oauth2_scheme)
):
    verify_token(token)
    logging.info("📥 Received query")
    text = parse_documents_from_url(payload.documents)

    results = []
    for question in payload.questions:
        answer = answer_question(text, question)
        results.append({"question": question, "answer": answer})

    return {"results": results}
