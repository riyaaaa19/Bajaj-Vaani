import os
from dotenv import load_dotenv
import google.generativeai as genai
from typing import List

load_dotenv()

def get_gemini_model():
    if not hasattr(get_gemini_model, "model"):
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise EnvironmentError("❌ GOOGLE_API_KEY not found in environment.")
        genai.configure(api_key=api_key)
        get_gemini_model.model = genai.GenerativeModel("models/gemini-1.5-flash")
    return get_gemini_model.model

def generate_response(query: str, clauses: List[str]) -> str:
    if not clauses:
        return "No relevant clauses found to answer the question."

    trimmed_clauses = [clause.strip()[:500] for clause in clauses if clause.strip()]

    # 🔍 Fallback: Try exact clause match
    for clause in trimmed_clauses:
        if any(word in clause.lower() for word in query.lower().split()):
            return clause.strip()

    prompt = f"""You are an expert insurance policy assistant. Use ONLY the clauses below to answer the user's question. DO NOT assume anything. Quote or paraphrase based on the given clauses only.

User Question:
{query}

Relevant Policy Clauses:
"""
    for idx, clause in enumerate(trimmed_clauses, 1):
        prompt += f"{idx}. {clause}\n"

    prompt += """

Respond with a short, accurate answer using the exact wording from the clauses when possible. Do NOT invent information. Say 'Not found' if unsure.
"""

    try:
        model = get_gemini_model()
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"❌ Gemini Error: {str(e)}"
