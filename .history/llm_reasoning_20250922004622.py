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

# Instantiate model
model = genai.GenerativeModel(  # type: ignore
    "gemini-1.5-flash",
    generation_config={"temperature": 0.3, "max_output_tokens": 512}
)

def clean_text(text: str) -> str:
    """
    Clean input text by removing extra spaces and line breaks.
    """
    return re.sub(r"\s+", " ", text).strip()

def answer_question(question: str, context: Optional[str] = None) -> str:
    """
    Ask Gemini for a professional, human-like answer.
    Includes context from a document if provided.
    Returns a readable and concise answer.
    """
    question = clean_text(question)
    if not question:
        return "Question is empty."

    # Build prompt for professional and user-friendly response
    prompt_lines = [
        "You are a helpful and professional AI assistant.",
        "Explain answers clearly and concisely without using examples or analogies.",
    ]
    if context:
        prompt_lines.append(f"Context from a document:\n{context}")
    prompt_lines.append(f"Question: {question}")
    prompt_lines.append("Answer:")

    prompt = "\n\n".join(prompt_lines)

    try:
        response = model.generate_content(prompt)  # type: ignore
        answer_text: str = (response.text or "").strip()

        # Optional: trim very long answers for better readability
        if len(answer_text.split()) > 150:
            answer_text = " ".join(answer_text.split()[:150]) + "..."

        return answer_text or "No answer returned by Gemini."

    except Exception as e:
        return f"Error generating answer: {e}"
