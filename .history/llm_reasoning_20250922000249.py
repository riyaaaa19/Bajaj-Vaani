# llm_reasoning.py
import os
import re
from typing import Optional
from dotenv import load_dotenv

# Google Gemini SDK
import google.generativeai as genai  # type: ignore
from google.generativeai.types import GenerationConfig  # type: ignore

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "").strip()
if not GOOGLE_API_KEY:
    raise RuntimeError("GOOGLE_API_KEY not set in environment variables")

# Configure Gemini API
genai.configure(api_key=GOOGLE_API_KEY)  # type: ignore

# Instantiate model with proper GenerationConfig
model = genai.GenerativeModel(
    "gemini-1.5-flash",
    generation_config=GenerationConfig(
        temperature=0.5,          # Controls randomness
        max_output_tokens=1500,   # Max length of response
        top_p=0.9,
        top_k=50
    )
)

def clean_question(question: str) -> str:
    """
    Clean input by removing extra spaces and line breaks.
    """
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
        response = model.generate_content(prompt)  # type: ignore
        answer_text: Optional[str] = (response.text or "").strip()
        if not answer_text:
            return "I couldn't find a detailed answer for this. Please try rephrasing your question."
        return answer_text
    except Exception as e:
        return f"Error generating answer: {e}"
