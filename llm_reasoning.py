import os
from dotenv import load_dotenv
import google.generativeai as genai
from typing import List

load_dotenv()

# 🔁 Lazy load Gemini model
def get_gemini_model():
    if not hasattr(get_gemini_model, "model"):
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise EnvironmentError("❌ GOOGLE_API_KEY not set.")
        genai.configure(api_key=api_key)
        get_gemini_model.model = genai.GenerativeModel("models/gemini-1.5-flash")
    return get_gemini_model.model

# 🧠 Generate concise answer using Gemini
def generate_response(query: str, clauses: List[str]) -> str:
    if not clauses:
        return "No relevant clauses available to answer this query."

    trimmed_clauses = [clause.strip()[:500] for clause in clauses if clause.strip()]

    prompt = f"""You are an expert insurance assistant. Use the following policy clauses to answer the user's question concisely and accurately.

User Question: {query}

Relevant Clauses:
"""
    for idx, clause in enumerate(trimmed_clauses, 1):
        prompt += f"{idx}. {clause}\n"

    prompt += "\nProvide a clear, fact-based answer."

    try:
        model = get_gemini_model()
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"❌ Gemini Error: {str(e)}"
