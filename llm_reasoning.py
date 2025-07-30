import os
import google.generativeai as genai
import re
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel(
    "gemini-1.5-flash",
    generation_config={"temperature": 0.4, "max_output_tokens": 200},
    safety_settings=[
        {"category": "HARM_CATEGORY_DEROGATORY", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_VIOLENCE", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_SEXUAL", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"}
    ]
)

def extract_relevant_clauses(text: str, question: str, max_clauses: int = 5) -> str:
    sentences = re.split(r"(?<=[.;])\s+", text)
    question_keywords = set(re.findall(r'\b\w+\b', question.lower()))
    
    scored = []
    for s in sentences:
        s_clean = s.strip()
        if len(s_clean) < 20:
            continue
        clause_words = set(re.findall(r'\b\w+\b', s_clean.lower()))
        score = len(question_keywords & clause_words)

        # domain-specific boosts
        bonus = 0
        if any(w in clause_words for w in ["grace", "premium", "payment", "days", "renew"]):
            bonus += 3
        if re.search(r"\b\d+\s*days\b", s_clean.lower()) or "thirty days" in s_clean.lower():
            bonus += 5

        scored.append((score + bonus, s_clean))

    top_clauses = [s for _, s in sorted(scored, reverse=True)[:max_clauses]]
    return "\n".join(top_clauses) if top_clauses else "No relevant clauses found."

def answer_question(text: str, question: str) -> str:
    context = extract_relevant_clauses(text, question)
    prompt = (
        f"{context}\n\n"
        f"Q: {question}\n"
        f"A: Answer only from the above and be very concise."
    )

    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"❌ LLM error: {e}"
