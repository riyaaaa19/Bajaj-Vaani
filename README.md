# 🛡️ Bajaj Vaani - Health Insurance AI Assistant

**Bajaj Vaani** is a FastAPI-based backend powered by Omnidimension AI and FAISS. It answers user queries about health insurance policies, extracts and indexes clauses from uploaded PDFs, and uses semantic search to provide clause-based reasoning.

---

## 🚀 Features

* **/query**: Ask natural language queries (e.g., "Is cataract surgery covered under this policy?")
* **/reasoning**: Provides reasoning-based responses using relevant indexed clauses
* **/upload**: Upload PDF policy documents and auto-index clauses using SentenceTransformer + FAISS

---

## 🧠 Technologies Used

* **FastAPI**
* **Omnidimension Python SDK**
* **FAISS** for vector-based clause retrieval
* **SentenceTransformer** (`all-MiniLM-L6-v2`)
* **Dotenv** for environment variable management

---

## 📁 Project Structure

```
📦bajaj_vaani_api
├── app.py                 # Main FastAPI application
├── query_agent.py         # Omnidimension API interface
├── llm_reasoning.py       # Prompt-based decision logic
├── vector_store.py        # FAISS indexing + search logic
├── document_parser.py     # PDF clause extractor
├── requirements.txt       # Dependencies
└── .env                   # API keys and config
```

---

## 📦 .env Format

```bash
OMNIDIMENSION_API_KEY=your_omnidim_api_key
OMNI_AGENT_ID=your_agent_id
```

---

## 🛠️ Setup & Run

```bash
git clone https://github.com/yourrepo/bajaj_vaani_api.git
cd bajaj_vaani_api

# Install dependencies
pip install -r requirements.txt

# Run the app
uvicorn app:app --reload
```

Access Swagger UI at: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🧪 Example Input

### /query

```json
{
  "text": "Is cataract surgery covered under this policy?"
}
```

### /reasoning

```json
{
  "text": "Will my hospitalization due to cataract surgery be reimbursed?"
}
```

### /upload

Upload PDF file with form-data key: `file`

---

## 🧩 Notes

* Ensure your `.env` file is configured properly with working API key and agent ID.
* Omnidimension SDK uses `client.agent.create()` and `client.agent.call()` for agent creation and querying.
* FAISS index (`index.faiss`) and corpus (`clauses.json`) are saved locally for persistence.

---

## 💬 Credits

Built with ❤️ for Bajaj Finserv's insurance assistant use case using Omnidimension's agent SDK and open-source NLP tools.
