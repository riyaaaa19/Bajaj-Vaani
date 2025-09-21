# llm_reasoning.py
import os
import re
from typing import Tuple
from dotenv import load_dotenv

# Import Google Gemini API
import google.generativeai as genai  # type: ignore

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "").strip()
if not GOOGLE_API_KEY:
    raise RuntimeError("GOOGLE_API_KEY not set in environment variables")

# Configure Gemini API
genai.configure(api_key=GOOGLE_API_KEY)  # type: ignore

# Instantiate model
model = genai.GenerativeModel(
    "gemini-1.5-flash",
    generation_config={"temperature": 0.3, "max_output_tokens": 512}
)  # type: ignore

def answer_question(question: str) -> str:
    """
    Ask Gemini directly for an answer to the question.
    Returns the answer as a string.
    """
    if not question.strip():
        return "Question is empty."

    prompt: str = (
        f"You are a helpful AI assistant. Answer the following question concisely:\n\n"
        f"Question: {question}\nAnswer:"
    )

    try:
        response = model.generate_content(prompt)  # type: ignore
        answer_text: str = (response.text or "").strip()
        return answer_text or "No answer returned by Gemini."
    except Exception as e:
        return f"Error generating answer: {e}"

# Optional helper to clean questions (remove extra spaces, line breaks)
def clean_question(question: str) -> str:
    return re.sub(r"\s+", " ", question).strip()
