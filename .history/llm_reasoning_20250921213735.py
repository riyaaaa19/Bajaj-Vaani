# llm_reasoning.py
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load API key
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "").strip()

# Configure Gemini
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel(
    "gemini-1.5-flash",
    generation_config={"temperature": 0.3, "max_output_tokens": 512}
)

def answer_question_direct(text: str, question: str) -> str:
    """
    Directly answer a question from the text using Gemini.
    """
    prompt = (
        "You are an expert assistant. "
        "Answer the question below based strictly on the text provided.\n\n"
        f"Text:\n{text}\n\n"
        f"Question: {question}\nAnswer:"
    )
    try:
        response = model.generate_content(prompt)
        return (response.text or "").strip()
    except Exception:
        return "Unable to extract relevant answer from document."
