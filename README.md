# 🛡️Bajaj Vaani - Policy Clause-Based Q\&A API

## Overview

Bajaj Vaani is an intelligent API designed to answer user queries based on policy documents. It extracts relevant clauses from uploaded insurance-related documents and uses Gemini AI to generate detailed answers for each question.

---

## Features

* ✅ Upload document via URL (PDF, DOCX, EML)
* ✅ Extract relevant clauses using semantic matching
* ✅ AI-generated clause-based answers using Google Gemini
* ✅ Optional JWT-based authentication
* ✅ FastAPI + Uvicorn-powered backend

---

## API Endpoint

**POST** `/hackrx/run`

### Request Body (JSON):

```json
{
  "documents": "https://example.com/sample.pdf",
  "questions": [
    "What is the grace period?",
    "Is policy cancellation allowed?"
  ]
}
```

### Response:

```json
{
  "answers": [
    "The grace period is 30 days after the due date...",
    "Yes, policy cancellation is permitted under..."
  ]
}
```

---

## Authentication (Optional)

* Add header: `Authorization: Bearer <token>`
* To generate token, use `/login` route (demo credentials in `.env`)

---

## Setup Instructions

1. Clone the repo
2. Install requirements: `pip install -r requirements.txt`
3. Add `.env` file with:

```
SECRET_KEY=your_secret_key
GOOGLE_API_KEY=your_gemini_key
VALID_USERNAME=admin
VALID_PASSWORD=admin123
```

4. Run the app: `uvicorn main:app --reload`
5. Visit `http://localhost:8000/docs` to test

---

## Deployment

The project is live on Render:
**Base URL:** `https://bajaj-vaani-y8dl.onrender.com`
**Swagger UI:** `/docs`
**API Endpoint:** `/hackrx/run`

---

## Team

Built for HackRx 5.0 by Team The Avalanche
