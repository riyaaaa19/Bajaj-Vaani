# llm_reasoning.py
import os
import re
from typing import Optional
from dotenv import load_dotenv

# Import Google Gemini API (suppress Pylance warnings)
import google.generativeai as genai  # type: ignore

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "").strip()
if not GOOGLE_API_KEY:
    raise RuntimeError("GOOGLE_API_KEY not set in environment variables")

# Configure Gemini API
genai.configure(api_key=GOOGLE_API_KEY)  # type: ignore

# Instantiate model (suppress Pylance warning)
model = genai.GenerativeModel(  # type: ignore
    "gemini-1.5-flash",
    generation_config={"temperature": 0.3, "max_output_tokens": 512}
)

def clean_question(question: str) -> str:
    """
    Clean the input question by removing extra spaces and line breaks.
    """
    return re.sub(r"\s+", " ", question).strip()

def answer_question(question: str, context: Optional[str] = None) -> str:
    """
    Ask Gemini directly for an answer to the question.
    Returns the answer as a detailed, friendly string.
    Optionally include context from a document.
    """
    question = clean_question(question)
    if not question:
        return "Question is empty."

    # Build a prompt that encourages Gemini to give a detailed and friendly answer
    prompt_lines = [
        "You are a helpful and friendly AI assistant.",
        "Provide a detailed, easy-to-understand, and human-like explanation.",
    ]
    if context:
        prompt_lines.append(f"Here is some context from a document:\n{context}")
    prompt_lines.append(f"Question: {question}")
    prompt_lines.append("Answer:")

    prompt = "\n\n".join(prompt_lines)

    try:
        response = model.generate_content(prompt)  # type: ignore
        answer_text: Optional[str] = (response.text or "").strip()
        return answer_text or "No answer returned by Gemini."
    except Exception as e:
        return f"Error generating answer: {e}"
