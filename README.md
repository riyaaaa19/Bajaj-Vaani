

### 🛡️ Bajaj Vaani: AI-Powered Insurance Reasoning API

---

#### 🚀 Overview

**Bajaj Vaani** is a FastAPI backend system that intelligently processes insurance documents and answers queries using semantic search and Gemini LLM-based reasoning.
Built for **HackRx 6.0** by **Team Avalanche**.

---

#### ✅ Features

**Document Handling**

* Upload PDFs, DOCX, or EML files
* Extract clauses using format-specific parsers
* Store vectors using FAISS

**Query & Reasoning**

* `/query`: Ask any insurance-related question
* `/reasoning`: Get LLM-powered decisions using matched clauses
* `/upload-and-ask`: Upload a policy and instantly ask questions

**Document Comparison**

* `/compare`: Compare two policies clause-wise using embeddings

**Authentication**

* JWT-based login system
* Dummy users stored in `users.json`
  Example:

  * `admin@example.com` / `adminpass`
  * `user@example.com` / `userpass`

**Semantic & AI Layer**

* FAISS + SentenceTransformer for clause matching
* Gemini 1.5 Flash API for contextual answers
* JSON outputs with justification & clause references

---

#### 🧪 Tech Stack

| Component        | Technology                         |
| ---------------- | ---------------------------------- |
| Backend          | FastAPI                            |
| Embedding Model  | all-MiniLM-L6-v2                   |
| Vector Store     | FAISS                              |
| LLM              | Gemini 1.5 Flash                   |
| Auth             | JWT + OAuth2                       |
| Containerization | Docker                             |
| Doc Parsing      | PyMuPDF, python-docx, email-parser |

---

#### 📦 API Endpoints

| Method | Endpoint           | Purpose                                    |
| ------ | ------------------ | ------------------------------------------ |
| POST   | `/login`           | Authenticate user and return access token  |
| POST   | `/query`           | Ask a general insurance question           |
| POST   | `/reasoning`       | Clause-matching + Gemini reasoning         |
| POST   | `/upload`          | Upload and extract clauses from a document |
| POST   | `/upload-and-ask`  | Upload a doc and ask question in one go    |
| POST   | `/compare`         | Compare two policy documents               |
| GET    | `/secure-endpoint` | Protected endpoint (requires JWT)          |

---

#### 🐳 Docker Instructions

1. **Build Docker Image**

   ```bash
   docker build -t bajaj-vaani-backend .
   ```

2. **Run the Container**

   ```bash
   docker run -p 8000:8000 --env-file .env bajaj-vaani-backend
   ```

---

#### 🧪 Local Development

1. **Clone the Repo**

   ```bash
   git clone https://github.com/riyaaaa19/Bajaj-Vaani.git
   cd Bajaj-Vaani
   ```

2. **Configure `.env` File**

   ```
   GEMINI_API_KEY=your_gemini_key_here
   SECRET_KEY=your_jwt_secret
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the App**

   ```bash
   uvicorn main:app --reload
   ```

---

#### 🔮 Future Scope

* Role-based access for admin/user
* Logging endpoint: `/logs`
* Policy query analytics dashboard
* Pinecone support for vector DB
* GitHub Actions for CI/CD

---
---

## 📑 API Documentation

Once the server is running, explore and test all endpoints using FastAPI's interactive Swagger UI:

**Open [http://localhost:8000/docs](http://localhost:8000/docs) in your browser**

This provides a user-friendly interface to try out all API routes, view request/response formats, and interact with Bajaj Vaani backend.

---

#### 👥 Team Avalanche – HackRx 6.0

Smart insurance understanding, powered by AI.
**\[Demo Link Coming Soon]**

---

