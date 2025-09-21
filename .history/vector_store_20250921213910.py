# vector_store.py
from typing import List
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss

class ClauseVectorStore:
    """
    Lightweight vector store for clauses using FAISS and SBERT.
    Fully type-hinted for Pylance/IDE safety.
    """

    clauses: List[str]
    index: faiss.IndexFlatL2
    model: SentenceTransformer

    def __init__(self, model_name: str = "paraphrase-MiniLM-L3-v2") -> None:
        """Initialize SBERT model and placeholders for clauses and FAISS index."""
        self.model = SentenceTransformer(model_name)
        self.index = None
        self.clauses = []

    def build_index(self, clauses: List[str]) -> None:
        """
        Build FAISS index from a list of clauses.
        """
        self.clauses = clauses
        embeddings: np.ndarray = self.model.encode(
            clauses, convert_to_numpy=True, show_progress_bar=False
        ).astype("float32")
        self.index = faiss.IndexFlatL2(embeddings.shape[1])
        self.index.add(embeddings)

    def query(self, question: str, top_k: int = 4) -> List[str]:
        """
        Query the top_k most relevant clauses for a question.
        """
        if self.index is None:
            raise ValueError("Index not built. Call build_index first.")

        q_emb: np.ndarray = self.model.encode([question], convert_to_numpy=True).astype("float32")
        
        # FAISS search returns distances and indices
        distances: np.ndarray
        indices: np.ndarray
        distances, indices = self.index.search(q_emb, top_k)  # type: ignore

        # Return the matched clauses safely
        return [self.clauses[i] for i in indices[0] if 0 <= i < len(self.clauses)]
