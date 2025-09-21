# llm_reasoning.py
import os
import re
from typing import Optional
from dotenv import load_dotenv
import google.generativeai as genai  # type: ignore

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "").strip()
if not GOOGLE_API_KEY:
    raise RuntimeError("GOOGLE_API_KEY not set in environment variables")

# Configure Gemini API
genai.configure(api_key=GOOGLE_API_KEY)  # type: ignore

MODEL_NAME = "gemini-1.5-flash"

def clean_question(question: str) -> str:
    """Clean the input question by removing extra spaces and line breaks."""
    return re.sub(r"\s+", " ", question).strip()

def answer_question(question: str, context: Optional[str] = None) -> str:
    """
    Ask Gemini for an answer to the question.
    Returns a detailed, friendly string.
    Optionally include context from a document.
    """
    question = clean_question(question)
    if not question:
        return "Question is empty."

    # Build messages for chat completion
    messages = [
        {
            "role": "system",
            "content": "You are a helpful and friendly AI assistant. "
                       "Provide detailed, easy-to-understand, human-like answers."
        }
    ]
    if context:
        messages.append({
            "role": "system",
            "content": f"Here is some context from a document:\n{context}"
        })

    messages.append({"role": "user", "content": question})

    try:
        response = genai.chat.completions.create(  # type: ignore
            model=MODEL_NAME,
            messages=messages,
            temperature=0.3,
            max_output_tokens=1024
        )
        # The assistant's reply
        answer_text = response.choices[0].message.get("content", "").strip()
        return answer_text or "No answer returned by Gemini."
    except Exception as e:
        return f"Error generating answer: {e}"
