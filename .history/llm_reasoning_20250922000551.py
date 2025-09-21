# llm_reasoning.py
import os
import re
from typing import Optional
from dotenv import load_dotenv
import google.generativeai as genai  # type: ignore

# Load API key
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "").strip()
if not GOOGLE_API_KEY:
    raise RuntimeError("GOOGLE_API_KEY not set")

# Configure API
genai.configure(api_key=GOOGLE_API_KEY)  # type: ignore
MODEL_ID = "gemini-1.5"

def clean_question(question: str) -> str:
    return re.sub(r"\s+", " ", question).strip()

def answer_question(question: str) -> str:
    """
    Ask Gemini for a friendly, detailed answer.
    """
    question = clean_question(question)
    if not question:
        return "Please provide a question."

    prompt = (
        "You are a helpful, friendly AI assistant. "
        "Answer in a detailed, easy-to-understand way, "
        "especially if the user provides documents. "
        f"Question: {question}\nAnswer:"
    )

    try:
        response = genai.generate_text(
            model=MODEL_ID,
            prompt=prompt,
            temperature=0.5,
            max_output_tokens=1500,
            top_p=0.9,
            top_k=50
        )
        # response.output_text contains the generated text
        answer_text = getattr(response, "output_text", None)
        return (answer_text or "I couldn't generate an answer.").strip()
    except Exception as e:
        return f"Error generating answer: {e}"
