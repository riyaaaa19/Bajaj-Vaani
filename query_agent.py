import os
from dotenv import load_dotenv
import google.generativeai as genai
from typing import List

# 🔐 Load API key
load_dotenv()

# 🚀 Lazy-load Gemini model
def get_gemini_model():
    if not hasattr(get_gemini_model, "model"):
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise EnvironmentError("❌ GOOGLE_API_KEY not found in environment.")
        genai.configure(api_key=api_key)
        get_gemini_model.model = genai.GenerativeModel("models/gemini-1.5-flash")
    return get_gemini_model.model

# 🧠 Generate concise LLM-based answer
def generate_response(query: str, clauses: List[str]) -> str:
    if not clauses:
        return "No relevant clauses found to answer the question."

    # ✂️ Token-efficient clause list
    trimmed_clauses = [clause[:500] for clause in clauses]

    prompt = f"""You are an expert insurance assistant. Use the following policy clauses to answer the user's question clearly and factually.

Question: {query}

Policy Clauses:
"""
    for idx, clause in enumerate(trimmed_clauses, 1):
        prompt += f"{idx}. {clause}\n"

    prompt += "\nPlease provide a concise answer backed by the clauses."

    try:
        model = get_gemini_model()
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"❌ Gemini Error: {str(e)}"
