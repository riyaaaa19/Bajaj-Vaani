# query_agent.py

import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load the .env file
load_dotenv()

# Fetch API key from .env
api_key = os.getenv("GOOGLE_API_KEY")
print("🔑 Loaded API Key:", api_key[:8] + "..." if api_key else "❌ NOT FOUND")

# Configure Gemini
genai.configure(api_key=api_key)

# Initialize model only once
try:
    model = genai.GenerativeModel("models/gemini-1.5-flash")
    print("✅ Gemini model loaded: models/gemini-1.5-flash")
except Exception as e:
    print("❌ Error loading Gemini model:", e)
    model = None

# Function to query Gemini
def query_bajaj_vaani(user_input: str):
    try:
        if not model:
            return "❌ Gemini model not loaded."
        response = model.generate_content(user_input)
        return response.text.strip()
    except Exception as e:
        return f"❌ Gemini AI error: {e}"
