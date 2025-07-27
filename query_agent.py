import os
from dotenv import load_dotenv
import google.generativeai as genai

# Lazy load Gemini model
def get_model():
    if not hasattr(get_model, "model"):
        load_dotenv()
        api_key = os.getenv("GOOGLE_API_KEY")
        print("🔑 Loaded API Key:", api_key[:8] + "..." if api_key else "❌ NOT FOUND")
        genai.configure(api_key=api_key)

        try:
            get_model.model = genai.GenerativeModel("models/gemini-1.5-flash")
            print("✅ Gemini model loaded: models/gemini-1.5-flash")
        except Exception as e:
            print("❌ Error loading Gemini model:", e)
            get_model.model = None

    return get_model.model

# 🔹 RAW query response (no reasoning)
def query_bajaj_vaani(user_input: str):
    model = get_model()
    if not model:
        return "❌ Gemini model not loaded."

    try:
        response = model.generate_content(user_input)
        return response.text.strip()
    except Exception as e:
        return f"❌ Gemini AI error: {e}"

# 🔁 Reasoned answer based on clauses
def generate_response(user_question: str, context_clauses: list[str]):
    model = get_model()
    if not model:
        return "❌ Gemini model not loaded."

    try:
        prompt = f"""You are a legal policy assistant.

Question: {user_question}

Relevant Clauses:
"""
        for idx, clause in enumerate(context_clauses, start=1):
            prompt += f"{idx}. {clause}\n"

        prompt += "\nBased on the above clauses, give a clear, accurate, and concise answer."

        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"❌ Gemini AI error: {e}"
