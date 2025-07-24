# 🛡️Bajaj Vaani: AI-Powered Insurance Reasoning Backend

## 🚀 Overview

Bajaj Vaani is an intelligent backend system that simplifies insurance policy understanding using LLM-powered reasoning, semantic clause matching, PDF/docx/email parsing, and secure access. Built for HackRx 6.0 by Team Avalanche.

---

## ✅ Features Checklist

### 🚀 Core Functionality
- [x] `POST /query`: Natural language insurance question answering
- [x] `POST /reasoning`: Gemini-powered clause reasoning using semantic matches
- [x] `POST /upload`: Upload PDF/docx/emails policies and extract/index clauses
- [x] `POST /compare`: Compare two policy documents clause-wise 🔧

### 🔐 Authentication
- [x] JWT-based login (`POST /login`)
- [x] Dummy users with roles (admin/user)
- [ ] Full role-based access control on protected routes 🔧
- [ ] User registration & password hashing 🔧

### 🧠 AI & Semantic Layer
- [x] Gemini 1.5 Flash integration for smart responses
- [x] FAISS + MiniLM for clause matching
- [x] Prompt templating for decision + explanation
- [ ] Multi-model support (fallback to local LLM or Claude) 🔧

### 📊 Admin & Logs
- [ ] Log requests to `logs.json`
- [ ] `GET /logs`: View logs via admin route 🔧
- [ ] Admin dashboard UI (FastAPI + Jinja/FastUI or external panel) 🔧

### 📦 Vector Store Management
- [x] Add clauses to vector DB (`add_clauses`)
- [x] Semantic search for top-k clauses (`search_similar_clauses`)
- [ ] Export indexed data to LangChain-compatible format 🔧

### 📈 Analytics (Planned)
- [ ] Track top queries over time 🔧
- [ ] Query coverage heatmap 🔧
- [ ] Most frequent clause triggers 🔧
- [ ] Admin insights for product teams 🔧

### ⚙️ DevOps
- [x] `.env` config for API keys
- [ ] Dockerized backend setup 🔧
- [ ] CI/CD GitHub Actions integration 🔧


---

## 🧠 How It Works

1. **PDF Clause Extraction** – Extracts text and segments it into clauses
2. **Semantic Search (FAISS + MiniLM)** – Finds most relevant clauses
3. **LLM Reasoning (Gemini)** – Gemini Flash model reasons over matches
4. **JWT Auth** – Secures all routes and logs user activity

---

## 🧪 Tech Stack

* **FastAPI** – Backend framework
* **Gemini 1.5 Flash** – LLM for QA and clause reasoning
* **SentenceTransformers + FAISS** – Vector similarity for clause search
* **SQLite / JSON** – Corpus & user storage
* **JWT** – Authentication & access control
* **Docker** – Containerized setup

---

## 🔐 Dummy Credentials

Stored in `users.json`

```json
{
  "admin@example.com": {
    "password": "adminpass",
    "role": "admin"
  },
  "user@example.com": {
    "password": "userpass",
    "role": "user"
  }
}
```

---

## 🧪 Running Locally

```bash
# 1. Clone repo
$ git clone https://github.com/riyaaaa19/Bajaj-Vaani.git
$ cd Bajaj-Vaani

# 2. Set up .env
GEMINI_API_KEY=your_key_here
SECRET_KEY=your_jwt_secret

# 3. Install dependencies
$ pip install -r requirements.txt

# 4. Run the app
$ uvicorn main:app --reload
```

---

## 🐳 Docker Setup

```bash
# Build Docker image
docker build -t bajaj-vaani .

# Run the container
docker run -p 8000:8000 --env-file .env bajaj-vaani
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
