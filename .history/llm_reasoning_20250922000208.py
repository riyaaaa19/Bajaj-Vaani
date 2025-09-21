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

# Instantiate model with updated generation_config
model = genai.GenerativeModel(  # type: ignore
    "gemini-1.5-flash",
    generation_config={
        "temperature": 0.7,          # slightly more creative
        "max_output_tokens": 1500,   # allow longer answers
        "top_p": 0.9,                # nucleus sampling for varied output
        "top_k": 50
    }
)

def clean_question(question: str) -> str:
    """
    Clean the input question by removing extra spaces and line breaks.
    """
    return re.sub(r"\s+", " ", question).strip()

def answer_question(question: str) -> str:
    """
    Ask Gemini for a friendly, easy-to-understand answer.
    """
    question = clean_question(question)
    if not question:
        return "Question is empty."

    prompt: str = (
        "You are a helpful, friendly, and knowledgeable AI assistant. "
        "Provide a clear, easy-to-understand, and detailed answer. "
        "Do not respond with just a few words; explain if needed in simple language. "
        "Use examples if relevant.\n\n"
        f"Context and question: {question}\n"
        "Answer:"
    )

    try:
        response = model.generate_content(prompt)  # type: ignore
        answer_text: Optional[str] = (response.text or "").strip()
        return answer_text or "No answer returned by Gemini."
    except Exception as e:
        return f"Error generating answer: {e}"
