# llm_reasoning.py
import os
import google.generativeai as genai
from dotenv import load_dotenv
from vector_store import ClauseVectorStore
import re

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "").strip()

# Configure Google Gemini
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel(
    "gemini-1.5-flash",
    generation_config={"temperature": 0.3, "max_output_tokens": 512}
)

def split_into_clauses(text: str) -> list[str]:
    """
    Splits text into clauses/sentences of meaningful length.
    """
    sentences = re.split(r"(?<=[.;])\s+", text)
    return [s.strip() for s in sentences if len(s.strip()) > 20]

def answer_question_with_clauses(text: str, question: str) -> tuple[str, str]:
    """
    Finds top relevant clauses using FAISS, asks Gemini for a concise answer.
    Returns (answer, used_clauses).
    """
    # Split document into clauses
    clauses = split_into_clauses(text)

    # Build FAISS index
    store = ClauseVectorStore()
    store.build_index(clauses)

    # Query for top clauses
    top_clauses = store.query(question, top_k=4)  # Reduced top_k for memory
    joined_clauses = "\n".join(top_clauses)

    # Prepare prompt for Gemini
    prompt = (
        "You are an expert insurance assistant. "
        "Based strictly on the extracted clauses below, answer the question "
        "clearly and concisely, listing conditions and exceptions if present.\n\n"
        f"Extracted Clauses:\n{joined_clauses}\n\n"
        f"Question: {question}\nAnswer:"
    )

    try:
        response = model.generate_content(prompt)
        answer_text = (response.text or "").strip()
        return answer_text, joined_clauses
    except Exception:
        return "Unable to extract relevant answer from document.", joined_clauses
