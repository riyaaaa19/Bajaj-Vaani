
# 🛡️ Bajaj Vaani – Chat-Based Insurance Assistant

Bajaj Vaani is an AI-powered FastAPI assistant for insurance document analysis. It semantically processes uploaded policies (PDF, DOCX, EML), answers user queries using Gemini 1.5, compares clauses across documents, and returns contextual explanations — all via secure JWT-authenticated endpoints.

---

## 🚀 Features

- 🔐 JWT-secured login with hardcoded user auth
- 📄 Upload & ask multiple questions from a single policy document
- 💬 Natural language query support
- 📊 Clause-wise policy comparison
- 🧠 Semantic clause matching with FAISS + MiniLM
- 🤖 Gemini-powered LLM explanations
- 🌐 Deployed via Docker + Render
- 🧪 Interactive Swagger UI at `/docs`

---

## 🧪 Quick Start

### 🔐 1. Login

**POST** `/login`  
Use the dummy judge account:

```bash
username: judge
password: demo123
````

**Response:**

```json
{
  "access_token": "your_token_here",
  "token_type": "bearer"
}
```

Use the token in the `Authorization` header for authenticated endpoints:

```
Authorization: Bearer your_token_here
```

---

### 📄 2. Upload & Ask Multiple Questions

**POST** `/run`

* Accepts a document via **file upload** or **blob URL**
* Accepts a list of **questions**

**Response:**

* AI-generated answers based on document clauses

---

## 💬 3. Query an Insurance Policy

**POST** `/ask`
**Auth Required:** ✅ JWT token (login via `/login`)

### 📥 Request Body

```json
{
  "text": "Does this policy cover accidental death?"
}
````

### 📤 Sample Response

```json
{
  "raw_answer": "Yes, the policy includes accidental death cover under section 5.",
  "explanation": "Clause 4.1 clearly states that the insured is entitled to compensation in case of accidental death. This satisfies your query."
}
```

### ✅ Behavior

* **`raw_answer`**: Direct response from **Google Gemini 1.5 Flash** (no clause context).
* **`explanation`**: Reasoned, clause-aware answer using **semantic search** from FAISS.

### 🧠 How it works

1. `query_bajaj_vaani()` gets the AI's raw response.
2. `search_similar_clauses()` finds relevant clauses from indexed policies.
3. `generate_response()` gives a precise explanation based on clause context.
---


### 📊 4. Compare Two Policy Documents

**POST** `/compare-from-blob`

```json
{
  "url1": "https://.../policy1.pdf",
  "url2": "https://.../policy2.pdf"
}
```

Returns:

* Sample clause matches
* Similarity score preview

---

## ⚙️ Tech Stack

* **Backend**: FastAPI
* **Vector Search**: FAISS + sentence-transformers (MiniLM)
* **LLM**: Google Gemini 1.5 Flash
* **Auth**: JWT (`python-jose`) with bcrypt
* **Parsing**: PyPDF2, python-docx, email
* **Deployment**: Docker + Render

---

## 🧪 Test the APIs

👉 Open [`/docs`](http://localhost:8000/docs) for the **FastAPI Swagger UI** to try all endpoints interactively.

---

## 🐳 Deployment

Build and run Docker:

```bash
docker build -t bajaj-vaani .
docker run -p 8000:8000 bajaj-vaani
```

On **Render**, ensure:

* Port 8000 is exposed
* `GEMINI_API_KEY` and `JWT_SECRET_KEY` are set as environment variables
* Add `EXPOSE 8000` in `Dockerfile`
* Use `numpy<2` for FAISS compatibility

---

## 👤 Author

Made with ❤️ by The Avalanche
Built for HackRx | Powered by Google Gemini + FAISS


