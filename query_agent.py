import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load the .env file
load_dotenv()

# Fetch API key
api_key = os.getenv("GEMINI_API_KEY")
print("🔑 Loaded API Key:", api_key[:8] + "..." if api_key else "❌ NOT FOUND")

# Configure Gemini
genai.configure(api_key=api_key)

# Optional: list models for debug
try:
    models = genai.list_models()
    if not models:
        print("⚠️ No models returned.")
    else:
        print("✅ Available Gemini Models:")
        for m in models:
            print("🔹", m.name)
except Exception as e:
    print("❌ Error listing models:", e)


# ✅ This is the function FastAPI expects in main.py
def query_bajaj_vaani(user_input: str):
    try:
        model = genai.GenerativeModel("models/gemini-1.5-flash")
        response = model.generate_content(user_input)
        return response.text.strip()
    except Exception as e:
        return f"❌ Gemini AI error: {e}"

