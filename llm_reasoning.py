import os
import google.generativeai as genai
import re
from dotenv import load_dotenv
load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

def extract_relevant_clauses(text: str, question: str, max_clauses: int = 5) -> str:
    # Split on sentence boundaries
    sentences = re.split(r"(?<=[.;])\s+", text)
    question_keywords = set(re.findall(r'\b\w+\b', question.lower()))

    scored = []
    for s in sentences:
        if len(s.strip()) < 20:
            continue
        clause_words = set(re.findall(r'\b\w+\b', s.lower()))
        score = len(question_keywords & clause_words)
        # Boost score if keywords like "grace", "premium", etc. match
        bonus = 0
        if "grace" in clause_words or "premium" in clause_words:
            bonus = 3
        scored.append((score + bonus, s.strip()))
    
    scored.sort(reverse=True)
    top_clauses = [s for _, s in scored[:max_clauses]]
    
    if not top_clauses:
        return "No relevant clauses found."
    
    return "\n".join(top_clauses)

def answer_question(text: str, question: str) -> str:
    context = extract_relevant_clauses(text, question)
    prompt = (
        "You are a helpful insurance assistant.\n\n"
        f"Relevant policy content:\n{context}\n\n"
        f"User's question: {question}\n\n"
        "Answer in one sentence using only the content above."
    )

    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"❌ LLM error: {e}"
