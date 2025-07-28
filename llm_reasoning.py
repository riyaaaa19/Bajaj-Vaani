import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

def get_gemini_model():
    if not hasattr(get_gemini_model, "model"):
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        get_gemini_model.model = genai.GenerativeModel("models/gemini-1.5-flash")
    return get_gemini_model.model

def generate_response(query: str, clauses: list[str]) -> str:
    prompt = f"""You are an expert insurance assistant. Using the following policy clauses, answer the user query accurately and briefly.

User Query: {query}

Relevant Policy Clauses:
"""

    for idx, clause in enumerate(clauses, start=1):
        prompt += f"{idx}. {clause}\n"

    prompt += "\nGive a concise and fact-based answer based on the above clauses."

    try:
        model = get_gemini_model()
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"❌ Gemini Error: {e}"
