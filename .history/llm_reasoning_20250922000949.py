import os
import re
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "").strip()
if not GOOGLE_API_KEY:
    raise RuntimeError("GOOGLE_API_KEY is not set in environment variables")

# Configure Gemini API
genai.configure(api_key=GOOGLE_API_KEY)  # type: ignore
MODEL_ID = "gemini-1.5"

def clean_question(question: str) -> str:
    """
    Clean the input question by removing extra spaces and line breaks.
    """
    return re.sub(r"\s+", " ", question).strip()

def answer_question(question: str) -> str:
    """
    Get a friendly, detailed answer from Gemini.
    """
    question = clean_question(question)
    if not question:
        return "Please provide a question."

    prompt = (
        "You are a helpful, friendly AI assistant. "
        "Provide a detailed and easy-to-understand answer, "
        "especially if the user provides a document for context. "
        f"Question: {question}\nAnswer:"
    )

    try:
        response = genai.generate_content(
            model=MODEL_ID,
            contents=prompt,
            config=types.GenerateContentConfig(
                max_output_tokens=512,
                temperature=0.3
            )
        )
        answer_text = response.text.strip()
        return answer_text or "No answer could be generated."
    except Exception as e:
        return f"Error generating answer: {e}"
