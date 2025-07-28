import os
from dotenv import load_dotenv
import google.generativeai as genai

def get_model():
    if not hasattr(get_model, "model"):
        load_dotenv()
        api_key = os.getenv("GOOGLE_API_KEY")
        genai.configure(api_key=api_key)
        get_model.model = genai.GenerativeModel("models/gemini-1.5-flash")
    return get_model.model

def generate_response(user_question: str, context_clauses: list[str]):
    model = get_model()
    try:
        prompt = f"""You are a legal insurance assistant.
User Question: {user_question}

Relevant Clauses:
"""
        for i, clause in enumerate(context_clauses, start=1):
            prompt += f"{i}. {clause}\n"

        prompt += "\nGive a concise, fact-based answer."
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"❌ Gemini Error: {e}"
