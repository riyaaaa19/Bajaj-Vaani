from sentence_transformers import SentenceTransformer
import numpy as np
import faiss

# Use a smaller model to reduce memory usage
MODEL_NAME = "paraphrase-MiniLM-L3-v2"

class ClauseVectorStore:
    def __init__(self):
        self.model = SentenceTransformer(MODEL_NAME)
        self.index = None
        self.clauses = []

    def build_index(self, clauses: list[str], batch_size: int = 100):
        self.clauses = clauses
        embeddings = []

        for i in range(0, len(clauses), batch_size):
            batch = clauses[i:i + batch_size]
            batch_embeddings = self.model.encode(batch, show_progress_bar=False)
            embeddings.extend(batch_embeddings)

        embeddings_np = np.array(embeddings).astype("float32")
        self.index = faiss.IndexFlatL2(embeddings_np.shape[1])
        self.index.add(embeddings_np)

    def query(self, query: str, top_k: int = 3) -> list[str]:
        query_embedding = self.model.encode([query]).astype("float32")
        distances, indices = self.index.search(query_embedding, top_k)

        return [self.clauses[i] for i in indices[0] if i < len(self.clauses)]
