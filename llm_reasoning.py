import os
import re
import google.generativeai as genai
from dotenv import load_dotenv
from vector_store import ClauseVectorStore

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel(
    "gemini-1.5-flash",
    generation_config={"temperature": 0.4, "max_output_tokens": 1024}
)

def split_into_clauses(text: str) -> list[str]:
    sentences = re.split(r"(?<=[.;])\s+", text)
    return [s.strip() for s in sentences if len(s.strip()) > 20]

def answer_question_with_clauses(text: str, question: str) -> tuple[str, str]:
    clauses = split_into_clauses(text)

    store = ClauseVectorStore()
    store.build_index(clauses, batch_size=100)  # Efficient batching
    top_clauses = store.query(question, top_k=3)

    prompt = (
        "You are an expert insurance assistant. Based only on the extracted clauses below, "
        "answer the question with accuracy, listing all conditions and exceptions clearly.\n\n"
        f"Extracted Clauses:\n{'\n'.join(top_clauses)}\n\n"
        f"Question: {question}\nAnswer:"
    )

    try:
        response = model.generate_content(prompt)
        return response.text.strip(), '\n'.join(top_clauses)
    except Exception:
        return "Unable to extract relevant answer from document.", '\n'.join(top_clauses)
