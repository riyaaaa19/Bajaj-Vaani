# llm_reasoning.py
import os
import re
from typing import Optional
from dotenv import load_dotenv

# Import Google Gemini API
import google.generativeai as genai  # type: ignore

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "").strip()
if not GOOGLE_API_KEY:
    raise RuntimeError("GOOGLE_API_KEY not set in environment variables")

# Configure API key
genai.configure(api_key=GOOGLE_API_KEY)  # type: ignore
MODEL_ID = "gemini-1.5"  # or "gemini-1.5-flash"

def clean_question(question: str) -> str:
    return re.sub(r"\s+", " ", question).strip()

def answer_question(question: str) -> str:
    """
    Ask Gemini for an answer.
    Returns a friendly, explanatory response.
    """
    question = clean_question(question)
    if not question:
        return "It looks like you didn't ask a question. Please provide a query so I can help!"

    prompt: str = (
        "You are a helpful, friendly AI assistant. "
        "Explain answers clearly, step by step if needed, "
        "so that a user without technical background can understand. "
        "Provide detailed context and examples where appropriate.\n\n"
        f"Question: {question}\nAnswer:"
    )

    try:
        response = genai.text.generate(
            model=MODEL_ID,
            prompt=prompt,
            temperature=0.5,
            max_output_tokens=1500,
            top_p=0.9,
            top_k=50
        )
        # In the new SDK, response has a 'candidates' list
        if response.candidates and len(response.candidates) > 0:
            answer_text = response.candidates[0].content.strip()
            return answer_text or "I couldn't generate an answer."
        return "I couldn't generate an answer."
    except Exception as e:
        return f"Error generating answer: {e}"
