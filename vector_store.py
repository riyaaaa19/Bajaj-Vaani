from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import re

# Use smaller model to save RAM
_model = None

def get_embedding_model():
    global _model
    if _model is None:
        _model = SentenceTransformer("paraphrase-MiniLM-L3-v2")
    return _model

def split_into_clauses(text: str) -> list[str]:
    # Limit to first 200 clauses to save memory
    sentences = re.split(r"(?<=[.;])\s+", text)
    return [s.strip() for s in sentences if len(s.strip()) > 20][:200]

class ClauseVectorStore:
    def __init__(self):
        self.index = None
        self.clauses = []

    def build_index(self, clauses: list[str]):
        model = get_embedding_model()
        self.clauses = clauses
        embeddings = model.encode(clauses, show_progress_bar=False, batch_size=16)
        dim = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dim)
        self.index.add(np.array(embeddings, dtype=np.float32))

    def query(self, question: str, top_k=3) -> list[str]:
        model = get_embedding_model()
        q_embed = model.encode([question], show_progress_bar=False)
        D, I = self.index.search(np.array(q_embed, dtype=np.float32), top_k)
        return [self.clauses[i] for i in I[0] if i < len(self.clauses)]
