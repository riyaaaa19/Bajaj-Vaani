
# 🛡️ Bajaj Vaani – LLM-Powered Insurance Query System

**Bajaj Vaani** is an intelligent LLM-based query-retrieval system designed to understand complex insurance documents like PDFs, DOCX, and emails. It provides accurate, clause-grounded answers to user questions by using Gemini Flash, FAISS-based semantic search, and policy clause extraction.

### 🔗 Try it Live
👉 [API Docs (Swagger UI)](https://bajaj-vaani-hjjc.onrender.com)

---

## 🚀 Features

- 📄 Parse PDF, DOCX, and EML documents from blob URLs
- 🤖 Answer policy-related questions using Gemini 1.5 Flash
- 🔍 Retrieve relevant clauses using semantic search (FAISS)
- ✅ Token-based authentication (via login endpoint)
- 🧠 Accurate, clause-based answers in real time
- ⚡ FastAPI backend with <30s average response time

---

## 📌 API Usage

### 🔐 Step 1: Login to get a token

POST `/login`

```json
{
  "username": "admin",
  "password": "admin123"
}
````

Response:

```json
{
  "access_token": "<your_token>",
  "token_type": "bearer"
}
```

In Swagger UI, click **Authorize** 🔐 and paste your token.

---

### 🤖 Step 2: Run Query

POST `/api/v1/bajaj-vaani/run`

```json
{
  "documents": "<blob_url_to_policy.pdf>",
  "questions": [
    "What is the grace period for premium payment?",
    "Does the policy cover maternity expenses?",
    ...
  ]
}
```

Response:

```json
{
  "results": [
    {
      "question": "...",
      "answer": "..."
    }
  ]
}
```

---

## ⚙️ Tech Stack

* **Backend**: FastAPI + Uvicorn
* **LLM**: Gemini 1.5 Flash (via Google Generative AI)
* **Vector DB**: FAISS
* **Parsing**: PyMuPDF, python-docx, BeautifulSoup
* **Auth**: OAuth2 (JWT)

---

## 🧠 Prompt Engineering

The system extracts top clauses from the document using keyword and semantic overlap, then crafts a concise prompt:

> “Based only on the above content, write a full, clause-based answer with all conditions and details.”

---

Made by - The Avalanche ✨

---



