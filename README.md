# 🛡️Bajaj Vaani: AI-Powered Insurance Reasoning Backend

## 🚀 Overview

Bajaj Vaani is an intelligent backend system that simplifies insurance policy understanding using LLM-powered reasoning, semantic clause matching, PDF parsing, and secure access. Built for HackRx 6.0 by Team Avalanche.

---

## 🔍 Features

### ✅ User-Facing APIs

* `POST /query` – Ask natural language questions like "Is cataract surgery covered?"
* `POST /reasoning` – Deep LLM-based analysis over relevant clauses
* `POST /upload` – Upload policy PDFs to extract and index clauses
* `POST /compare` – Compare coverage between two policy documents

### 🔐 Authentication

* `POST /login` – JWT-based login system
* Role-based (Admin/User) access management *(optional)*

### ⚙️ Admin APIs

* `GET /logs` – View request logs (admin-only)

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
