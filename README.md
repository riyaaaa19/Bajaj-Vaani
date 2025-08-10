

# 📜 Bajaj Vaani – Clause-Based QA API

An API that extracts relevant clauses from insurance documents and answers user questions using **FAISS-based semantic search** and **Google Gemini 1.5 Flash**.

---

## 🚀 Features

* 📄 **Document Parsing** – Supports PDF, DOCX, and EML formats.
* 🔍 **Semantic Search** – Finds relevant clauses using `SentenceTransformer` + FAISS.
* 🤖 **LLM Integration** – Generates accurate answers with Gemini 1.5 Flash.
* 🔐 **Secure API** – Bearer Token authentication as per HackRx PS.
* ⚡ **Optimized for Deployment** – Memory-efficient clause indexing.

---

## 📌 API Endpoint

**POST**

```
https://bajaj-vaani-y8dl.onrender.com/api/v1/hackrx/run
```

### **Headers**

```
Authorization: Bearer 8c4bbc30a45570cc5b1e605cba9c98db4ca91fd254c9d612ebf43e051302194d
Content-Type: application/json
```

### **Request Body**

```json
{
  "documents": "https://example.com/sample.pdf",
  "questions": [
    "What is the claim settlement process?",
    "List the exclusions mentioned in the policy."
  ]
}
```

### **Response**

```json
{
  "answers": [
    "Claims can be made by notifying the insurer, submitting forms and documents...",
    "The policy excludes damage due to war, terrorism, and pre-existing conditions..."
  ]
}
```

---

## 🛠️ Installation (Local Setup)

```bash
git clone https://github.com/<your-username>/<repo-name>.git
cd <repo-name>
pip install -r requirements.txt
uvicorn main:app --reload
```

---

## 📂 Project Structure

```
├── main.py               # FastAPI entry point
├── vector_store.py       # FAISS vector store logic
├── llm_reasoning.py      # LLM-based reasoning and answer generation
├── document_parser.py    # Document parsing for PDF, DOCX, EML
├── auth.py               # Token verification
├── requirements.txt
└── README.md
```

---

## 📄 License

This project is developed for **HackRx** and is intended for demonstration purposes only.
