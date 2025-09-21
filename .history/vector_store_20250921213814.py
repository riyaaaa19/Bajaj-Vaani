# vector_store.py
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

class ClauseVectorStore:
    def __init__(self, model_name="paraphrase-MiniLM-L3-v2"):
        """Lightweight SBERT model for clause embeddings."""
        self.model = SentenceTransformer(model_name)
        self.index = None
        self.clauses = []

    def build_index(self, clauses: list[str]):
        """Build FAISS index from clauses."""
        self.clauses = clauses
        embeddings = self.model.encode(clauses, convert_to_numpy=True, show_progress_bar=False)
        embeddings = embeddings.astype("float32")
        self.index = faiss.IndexFlatL2(embeddings.shape[1])
        self.index.add(embeddings)

    def query(self, question: str, top_k=4):
        """Return top_k most relevant clauses."""
        if self.index is None:
            raise ValueError("Index not built. Call build_index first.")
        q_emb = self.model.encode([question], convert_to_numpy=True).astype("float32")
        distances, indices = self.index.search(q_emb, top_k)
        return [self.clauses[i] for i in indices[0] if 0 <= i < len(self.clauses)]
