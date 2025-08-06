# vector_store.py

from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import hashlib

# Load model once
model = SentenceTransformer("all-MiniLM-L6-v2")

# Global cache {hash -> ClauseVectorStore}
index_cache = {}

def get_text_hash(text: str) -> str:
    return hashlib.md5(text.encode()).hexdigest()

class ClauseVectorStore:
    def __init__(self, clauses: list[str]):
        self.clauses = clauses
        self.embeddings = model.encode(clauses, convert_to_numpy=True, show_progress_bar=False)
        self.index = faiss.IndexFlatL2(self.embeddings.shape[1])
        self.index.add(self.embeddings)

    def query(self, question: str, top_k: int = 5) -> list[str]:
        question_vec = model.encode([question], convert_to_numpy=True)
        _, I = self.index.search(question_vec, top_k)
        return [self.clauses[i] for i in I[0]]

def get_or_build_index(text: str) -> ClauseVectorStore:
    text_hash = get_text_hash(text)
    if text_hash not in index_cache:
        print("[INFO] Building new FAISS index...")
        clauses = [c.strip() for c in text.splitlines() if len(c.strip()) > 20]
        index_cache[text_hash] = ClauseVectorStore(clauses)
    else:
        print("[INFO] Reusing cached FAISS index.")
    return index_cache[text_hash]
