# Bajaj Vaani – Intelligent Finance Chatbot

**Bajaj Vaani** is an AI-powered finance assistant designed to help users interactively understand financial and insurance-related queries. The chatbot leverages **Google Gemini** for reasoning, provides persistent document context for multiple queries, and supports PDF, DOCX, and TXT uploads for enhanced understanding.

---

## Table of Contents

1. [Overview](#overview)
2. [Features](#features)
3. [Technology Stack](#technology-stack)
4. [Installation](#installation)
5. [Usage](#usage)
6. [API Endpoints](#api-endpoints)
7. [Architecture & Data Flow](#architecture--data-flow)
8. [Future Scope](#future-scope)
9. [References](#references)

---

## Overview

Bajaj Vaani provides users with an interactive and human-like financial assistant experience. Users can ask questions, upload policy or finance documents, and receive **detailed, friendly, and easy-to-understand explanations**. The system maintains context across multiple queries, allowing seamless interactions about previously uploaded documents.

---

## Features

* Text-based question answering with persistent context
* Document upload for PDFs, DOCX, and TXT files
* Detailed, human-friendly explanations for financial queries
* JWT-based authentication for secure access
* Logging of all queries and responses
* RESTful API architecture for frontend-backend integration

---

## Technology Stack

* **Frontend:** React, Tailwind CSS, HTML5, JavaScript
* **Backend:** FastAPI (Python), Uvicorn server
* **Database:** PostgreSQL for user accounts and document storage
* **AI / LLM:** Google Gemini
* **Document Parsing:** PyPDF2 (PDF), python-docx (DOCX), standard text processing
* **Authentication & Security:** JWT-based Bearer Tokens, HTTPS
* **APIs:** RESTful endpoints for chat and document upload

---

## Installation

1. **Clone the repository:**

```bash
git clone <repository-url>
cd bajaj-vaani
```

2. **Create and activate a virtual environment:**

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. **Install dependencies:**

```bash
pip install -r requirements.txt
```

4. **Set up environment variables:**

```env
GOOGLE_API_KEY=<Your-Google-API-Key>
DATABASE_URL=postgresql://<user>:<password>@<host>:<port>/<database>
```

5. **Initialize the database:**

```bash
python -m backend.create_admin
```

6. **Run the application:**

```bash
uvicorn main:app --reload
```

---

## Usage

* Navigate to `http://localhost:8000` (or frontend URL if integrated).
* Register and login using your credentials.
* Ask questions directly via text or upload documents to provide additional context.
* The chatbot will answer in a **detailed, friendly, and easy-to-understand manner**.

---

## API Endpoints

| Endpoint    | Method | Description                           |
| ----------- | ------ | ------------------------------------- |
| `/register` | POST   | Register a new user                   |
| `/login`    | POST   | Login and get JWT token               |
| `/chat`     | POST   | Ask a question (text-only)            |
| `/upload`   | POST   | Upload document(s) and ask a question |

---

## Architecture & Data Flow

1. **User sends a query or uploads a document** via the frontend.
2. **Backend authenticates** the user using JWT tokens.
3. **Document content is extracted** using PyPDF2 or python-docx and stored as context.
4. **Query + context** is sent to Google Gemini for reasoning.
5. **Response** is logged and returned to the user in a human-friendly format.

---

## Future Scope

* Deploy on **cloud platforms** like AWS, Render, or Heroku.
* Add **multi-language support** for queries.
* Integrate with **voice assistants** using TTS and speech recognition.
* Implement **analytics dashboard** for query patterns and document usage.

---

## References

1. [Google Gemini Documentation](https://developers.generativeai.google/)
2. [FastAPI Documentation](https://fastapi.tiangolo.com/)
3. [PyPDF2 Documentation](https://pypdf2.readthedocs.io/)
4. [python-docx Documentation](https://python-docx.readthedocs.io/)
5. [JWT Authentication](https://jwt.io/introduction/)
6. [Finance & Insurance Policies](https://www.bajajfinserv.in/insurance)
