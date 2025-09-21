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
    raise RuntimeError("GOOGLE_API_KEY not set")

# Configure API
genai.configure(api_key=GOOGLE_API_KEY)

# Use GenerativeModel for query generation
model = genai.GenerativeModel(
    "gemini-1.5-flash",
    generation_config={"temperature": 0.3, "max_output_tokens": 512}
)

def clean_question(question: str) -> str:
    return re.sub(r"\s+", " ", question).strip()

def answer_question(question: str, context: Optional[str] = None) -> str:
    question = clean_question(question)
    if not question:
        return "Question is empty."

    prompt_lines = [
        "You are a helpful and friendly AI assistant.",
        "Provide a detailed, easy-to-understand explanation."
    ]
    if context:
        prompt_lines.append(f"Context:\n{context}")
    prompt_lines.append(f"Question: {question}")
    prompt_lines.append("Answer:")

    prompt = "\n\n".join(prompt_lines)

    try:
        response = model.generate_content(prompt)  # Correct method
        answer_text = (response.text or "").strip()
        return answer_text or "No answer returned by Gemini."
    except Exception as e:
        return f"Error generating answer: {e}"
