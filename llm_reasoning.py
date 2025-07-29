import os
import google.generativeai as genai
from dotenv import load_dotenv
from typing import List

load_dotenv()

def get_gemini_model():
    if not hasattr(get_gemini_model, "model"):
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        get_gemini_model.model = genai.GenerativeModel("models/gemini-1.5-flash")
    return get_gemini_model.model

def generate_response(question: str, clauses: List[str]) -> str:
    if not clauses:
        return "Not found."

    prompt = (
        f"You are an insurance policy assistant. Use the following clauses to answer the question below.\n\n"
        f"Question: {question}\n\n"
        f"Relevant Clauses:\n"
    )
    for idx, clause in enumerate(clauses[:5], 1):
        prompt += f"{idx}. {clause.strip()[:500]}\n"

    prompt += "\nGive a concise, factual answer using clause language. Say 'Not found.' if not answerable."

    try:
        model = get_gemini_model()
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"❌ Gemini Error: {str(e)}"
