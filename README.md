# 🛡️ Bajaj Vaani – Insurance Query Resolution Assistant

## 📖 Overview

**Bajaj Vaani** is a voice and text-based insurance assistant that helps users inquire about their Bajaj Finserv health insurance policy coverage. It uses an intelligent agent powered by the **Omnidimension SDK** for reasoning, **Deepgram** for live transcription, and **ElevenLabs** for voice synthesis.

## 🚀 Features

* Clause-level query resolution
* Voice & text support
* Multilingual (English, Hindi, Marathi)
* Live transcription using Deepgram
* Natural-sounding TTS using ElevenLabs
* Policy clause retrieval with FAISS
* Post-call summarization and email support

## 🧠 Powered By

* **Omnidimension SDK** (GPT-4o-mini)
* **Deepgram** (Streaming ASR)
* **ElevenLabs** (Text-to-Speech)
* **FAISS** (Semantic clause matching)

## 📦 Requirements

Install the dependencies:

```bash
pip install -r requirements.txt
```

Your `requirements.txt` should include:

```
fastapi
uvicorn
openai
omnidimension
python-dotenv
faiss-cpu
sentence-transformers
PyMuPDF
```

## 🔐 Environment Setup

Create a `.env` file with the following keys:

```
OMNIDIMENSION_API_KEY=<your_omnidimension_key>
OMNI_AGENT_ID=<your_agent_id>
```

> Do not commit `.env` with real credentials.

## 🛠️ Agent Creation

Use `create_agent.py` to define your agent in Omnidimension:

```python
from omnidimension import Client

client = Client(api_key)
response = client.agent.create(
    name="Bajaj Vaani",
    # full configuration with context_breakdown, transcriber, model, voice, post_call_actions
)
```

This returns your **Agent ID** which you’ll use in production.

## 🎙️ Running the FastAPI Server

```bash
uvicorn main:app --reload
```

Query the bot:

```bash
curl -X POST "http://localhost:8000/query?text=46-year-old male, knee surgery, 3-month-old policy"
```

## 🧰 Example Output

```json
{
  "response": {
    "decision": "Covered",
    "explanation": "Knee surgery is covered after a 3-month waiting period.",
    "conditions": "Not valid if cosmetic."
  }
}
```

## 🩱 Architecture Flow

1. User query → `/query` endpoint
2. FAISS matches policy clauses
3. Agent (Omnidimension) evaluates coverage
4. Responds with structured markdown
5. Optionally triggers TTS and post-call actions

## 📬 Post-Call Actions

* Email summary to user
* Extract variables (age, policy age, decision, language)

## 📌 Notes

* This version **uses Omnidimension SDK**, not OpenAI directly.
* Deepgram & ElevenLabs credentials are handled within the Omnidimension agent config.
* Voice pipeline, transcription, and summarization handled server-side by the agent.

## 🙌 Contributions

For contributions, contact the author or raise an issue in your private repo.

## 📞 Example Query

> "My mother is 60, had cataract surgery, policy is 4 months old"

## ✅ License

Internal Use – Bajaj Finserv / Riya Saraf
