# 🛡️ Bajaj Vaani: AI-Powered Insurance Reasoning Backend

## 🚀 Overview
Bajaj Vaani is an intelligent backend system that simplifies insurance policy understanding using LLM-powered reasoning, semantic clause matching, PDF/docx/eml parsing, and secure access. Built for HackRx 6.0 by Team Avalanche.

---

## ✅ Features Checklist

### 🚀 Core Functionality
- [x] `POST /query`: Natural language insurance question answering
- [x] `POST /reasoning`: Gemini-powered clause reasoning using semantic matches
- [x] `POST /upload`: Upload PDF/docx/eml policies and extract/index clauses
- [x] `POST /compare`: Compare two policy documents clause-wise
- [x] `POST /upload-and-ask`: Upload a document and ask multiple questions in one request

### 🔐 Authentication
- [x] JWT-based login (`POST /login`)
- [x] Dummy users with roles (admin/user)
- [ ] Full role-based access control on protected routes
- [ ] User registration & password hashing

### 🧠 AI & Semantic Layer
- [x] Gemini 1.5 Flash integration for smart responses
- [x] FAISS + MiniLM for clause matching
- [x] Prompt templating for decision + explanation
- [ ] Multi-model support (fallback to local LLM or Claude)

### 📊 Admin & Logs
- [ ] Log requests to `logs.json`
- [ ] `GET /logs`: View logs via admin route
- [ ] Admin dashboard UI (FastAPI + Jinja/FastUI or external panel)

### 📦 Vector Store Management
- [x] Add clauses to vector DB (`add_clauses`)
- [x] Semantic search for top-k clauses (`search_similar_clauses`)
- [ ] Export indexed data to LangChain-compatible format

### 📈 Analytics (Planned)
- [ ] Track top queries over time
- [ ] Query coverage heatmap
- [ ] Most frequent clause triggers
- [ ] Admin insights for product teams

### ⚙️ DevOps
- [x] `.env` config for API keys
- [x] Dockerized backend setup
- [ ] CI/CD GitHub Actions integration

---

## 🧠 How It Works
1. **PDF/docx/eml Clause Extraction** – Extracts text and segments it into clauses
2. **Semantic Search (FAISS + MiniLM)** – Finds most relevant clauses
3. **LLM Reasoning (Gemini)** – Gemini Flash model reasons over matches
4. **JWT Auth** – Secures all routes and logs user activity

---

## 🧪 Tech Stack
* **FastAPI** – Backend framework
* **Gemini 1.5 Flash** – LLM for QA and clause reasoning
* **SentenceTransformers + FAISS** – Vector similarity for clause search
* **JWT** – Authentication & access control
* **Docker** – Containerized setup

---

## 🔐 Dummy Credentials
Stored in `auth.py`:

```python
fake_users_db = {
    "judge": {
        "username": "judge",
        "full_name": "Hackathon Judge",
        "hashed_password": "$2b$12$RjGJN1TegbzUyvKqJzNDkOvRgiYcOmNfIuSW93CIDGABtZCKdB1fm",  # "demo123"
        "role": "admin"
    }
}
```

---

## 🧪 Running Locally

```bash
# 1. Clone repo
git clone https://github.com/riyaaaa19/Bajaj-Vaani.git
cd Bajaj-Vaani

# 2. Set up .env
GOOGLE_API_KEY=your_key_here
SECRET_KEY=your_jwt_secret

# 3. Install dependencies
pip install -r 

# 4. Run the app
uvicorn main:app --reload
```

---

## 🐳 Docker Setup

```bash
# Build Docker image
docker build -t bajaj-vaani-backend .

# Run the container
docker run -p 8000:8000 --env-file .env bajaj-vaani-backend
```

---

## 🧠 Future Scope

* LangChain export for smart chains
* Analytics dashboard with policy trends
* Role-based admin panel
* Support for other document types (Legal, Healthcare)

---

## 📞 Contact

Team Avalanche | Built for HackRx 6.0
 | [Demo Link Coming Soon]
