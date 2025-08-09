import os
import google.generativeai as genai
from dotenv import load_dotenv
from vector_store import ClauseVectorStore, split_into_clauses

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel(
    "gemini-1.5-flash",
    generation_config={"temperature": 0.4, "max_output_tokens": 512}  # reduce tokens
)

def answer_question_with_clauses(text: str, question: str) -> tuple[str, str]:
    clauses = split_into_clauses(text)
    store = ClauseVectorStore()
    store.build_index(clauses)
    top_clauses = store.query(question, top_k=3)
    joined_clauses = "\n".join(top_clauses)

    prompt = (
        "You are an expert insurance assistant. Based only on the extracted clauses below, "
        "answer the question clearly.\n\n"
        f"Extracted Clauses:\n{joined_clauses}\n\n"
        f"Question: {question}\nAnswer:"
    )

    try:
        response = model.generate_content(prompt)
        return response.text.strip(), joined_clauses
    except Exception:
        return "Unable to extract relevant answer.", joined_clauses
