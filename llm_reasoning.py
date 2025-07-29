import google.generativeai as genai
import numpy as np
import faiss
from vector_store import embedder
import os

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

def get_llm_answer(question: str, index_data):
    q_embedding = embedder.encode([question], convert_to_numpy=True)
    D, I = index_data["index"].search(q_embedding, k=3)
    matched_clauses = [index_data["clauses"][i] for i in I[0]]

    prompt = (
        "Based on the following clauses from the insurance document, answer the question as accurately as possible.\n\n"
        + "\n\n".join(matched_clauses)
        + f"\n\nQuestion: {question}\nAnswer:"
    )

    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error: {str(e)}"
