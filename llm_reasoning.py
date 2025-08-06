# llm_reasoning.py

import os
import google.generativeai as genai
from dotenv import load_dotenv
from vector_store import get_or_build_index
import re

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel(
    "gemini-1.5-flash",
    generation_config={"temperature": 0.4, "max_output_tokens": 1024}
)

def answer_question_with_clauses(full_text: str, question: str) -> tuple[str, str]:
    store = get_or_build_index(full_text)
    top_clauses = store.query(question, top_k=6)
    joined_clauses = "\n".join(top_clauses)

    prompt = (
        "You are an expert insurance assistant. Based only on the extracted clauses below, "
        "answer the question with accuracy, listing all conditions and exceptions clearly.\n\n"
        f"Extracted Clauses:\n{joined_clauses}\n\n"
        f"Question: {question}\nAnswer:"
    )

    try:
        response = model.generate_content(prompt)
        return response.text.strip(), joined_clauses
    except Exception as e:
        return "Unable to extract relevant answer from document.", joined_clauses
