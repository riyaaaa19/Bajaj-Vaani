# vector_store.py
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

class ClauseVectorStore:
    def __init__(self, model_name="paraphrase-MiniLM-L3-v2"):
        """
        Uses a smaller SBERT model for memory efficiency (around 80MB in RAM).
        """
        self.model = SentenceTransformer(model_name)
        self.index = None
        self.clauses = []

    def build_index(self, clauses: list[str]):
        """
        Builds FAISS index from clauses in smaller batches to save memory.
        """
        self.clauses = clauses
        embeddings = []
        batch_size = 32  # small batches to avoid high memory peaks

        for i in range(0, len(clauses), batch_size):
            batch = clauses[i:i + batch_size]
            emb = self.model.encode(batch, convert_to_numpy=True, show_progress_bar=False)
            embeddings.append(emb)

        embeddings = np.vstack(embeddings).astype("float32")
        self.index = faiss.IndexFlatL2(embeddings.shape[1])
        self.index.add(embeddings)

    def query(self, question: str, top_k=4):
        """
        Returns top_k most relevant clauses.
        """
        if not self.index:
            raise ValueError("Index not built. Call build_index first.")
        q_emb = self.model.encode([question], convert_to_numpy=True)
        distances, indices = self.index.search(q_emb.astype("float32"), top_k)
        return [self.clauses[i] for i in indices[0] if 0 <= i < len(self.clauses)]
