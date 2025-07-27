# 🛡️ Bajaj Vaani – Chat-Based Insurance Assistant

**Bajaj Vaani** is an AI-powered FastAPI assistant for insurance document analysis. It semantically processes uploaded policies (PDF, DOCX, EML), answers user queries using Gemini 1.5, compares clauses across documents, and returns contextual explanations — all via secure JWT-authenticated endpoints.

🌐 **Live App**: [https://huggingface.co/spaces/riyaaa19/bajaj-vaani-api](https://huggingface.co/spaces/riyaaa19/bajaj-vaani-api)

---

## 🚀 Features  
🔐 JWT-secured login with hardcoded user auth  
📄 Upload & ask multiple questions from a single policy document  
💬 Natural language query support  
📊 Clause-wise policy comparison  
🧠 Semantic clause matching with FAISS + MiniLM  
🤖 Gemini-powered LLM explanations  
🧪 Interactive Swagger UI at `/`

---

## 🧪 Quick Start  
🔐 1. Login  
**POST** `/login`  
Use the dummy judge account:

```json
{
  "username": "judge",
  "password": "demo123"
}
````

Use the token in the Authorization header:

```
Authorization: Bearer your_token_here
```

📄 2. Upload & Ask Multiple Questions
**POST** `/run`

* Accepts a document (file or blob URL)
* Accepts a list of questions
* Returns Gemini-powered answers based on document clauses

💬 3. Query an Insurance Policy
**POST** `/ask` *(Auth Required)*

**Request**

```json
{ "text": "Does this policy cover accidental death?" }
```

**Response**

```json
{
  "explanation": "Clause 4.1 clearly states that the insured is entitled to compensation in case of accidental death. This satisfies your query."
}
```

🧠 How it works

* `search_similar_clauses()` finds relevant clauses from indexed policies
* `generate_response()` gives a precise explanation using Gemini + clause context

📊 4. Compare Two Policy Documents
**POST** `/compare-from-blob`

```json
{
  "url1": "https://.../policy1.pdf",
  "url2": "https://.../policy2.pdf"
}
```

Returns: Sample clause matches + similarity scores

---

## ⚙️ Tech Stack

* **Backend**: FastAPI
* **Vector Search**: FAISS + `sentence-transformers` (MiniLM)
* **LLM**: Google Gemini 1.5 Flash
* **Auth**: JWT (`python-jose`) with bcrypt
* **Parsing**: PyPDF2, python-docx, email
* **Deployment**: Hugging Face Spaces (Gradio + FastAPI runtime)

---

## 🐳 Deployment
✅ App is hosted and running live on **Hugging Face Spaces**
🔗 [https://huggingface.co/spaces/riyaaa19/bajaj-vaani-api](https://huggingface.co/spaces/riyaaa19/bajaj-vaani-api)

---

## 👤 Author
Made with ❤️ by The Avalanche
Built for HackRx | Powered by Google Gemini + FAISS


