import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

# --- Lazy Gemini Loader ---
def get_gemini_model():
    if not hasattr(get_gemini_model, "model"):
        api_key = os.getenv("GOOGLE_API_KEY")
        genai.configure(api_key=api_key)
        get_gemini_model.model = genai.GenerativeModel("models/gemini-1.5-flash")
    return get_gemini_model.model

# --- Main Inference Function ---
def generate_response(query: str, clauses: list[str]) -> str:
    prompt = f"""You are an expert insurance assistant. Use the following policy clauses to answer the user's question accurately and concisely.

User Question: {query}

Relevant Clauses:
"""
    for idx, clause in enumerate(clauses, 1):
        prompt += f"{idx}. {clause}\n"

    prompt += "\nGive a clear, fact-based answer using the above context."

    try:
        model = get_gemini_model()
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"❌ Gemini Error: {e}"
