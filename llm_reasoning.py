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
    query_lower = query.lower().split()

    # 🔍 Prefer clause match if overlap > 75%
    for clause in trimmed_clauses:
        match_score = sum(word in clause.lower() for word in query_lower)
        if match_score / len(query_lower) > 0.75:
            return clause.strip()[:300]  # return summarized clause

    # 🤖 Gemini fallback
    prompt = f"""You are an expert insurance policy assistant. Use ONLY the clauses below to answer the user's question. DO NOT assume anything.

User Question:
{query}

Relevant Policy Clauses:
"""
    for idx, clause in enumerate(trimmed_clauses, 1):
        prompt += f"{idx}. {clause}\n"

    prompt += """

Summarize the answer in one or two sentences only. Use exact language from the clauses if possible. Do NOT invent information. Say 'Not found' if unsure.
"""

    try:
        model = get_gemini_model()
        response = model.generate_content(prompt)
        raw = response.text.strip()

        # ✂️ Force truncation to max 2 sentences
        sentences = raw.split('. ')
        short_summary = '. '.join(sentences[:2])
        return short_summary.strip().rstrip('.') + '.'

    except Exception as e:
        return f"❌ Gemini Error: {str(e)}"
