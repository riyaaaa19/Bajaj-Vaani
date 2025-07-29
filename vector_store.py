import os
import faiss
import pickle
from typing import List, Tuple
from sentence_transformers import SentenceTransformer

faiss_path = "faiss_index"
index_file = os.path.join(faiss_path, "faiss.index")
meta_file = os.path.join(faiss_path, "faiss.meta")

model = SentenceTransformer("all-MiniLM-L6-v2")
index = None
metadata = []

def initialize_vector_store():
    global index, metadata
    if not os.path.exists(index_file):
        os.makedirs(faiss_path, exist_ok=True)
        index = faiss.IndexFlatL2(384)
        metadata = []
        return
    index = faiss.read_index(index_file)
    with open(meta_file, "rb") as f:
        metadata = pickle.load(f)

def add_clauses(clauses: List[str], source_file: str):
    vectors = model.encode(clauses, show_progress_bar=False)
    index.add(vectors)
    metadata.extend([(clause, source_file) for clause in clauses])
    save_vector_store()

def build_faiss_index(clauses: List[Tuple[str, str]], batch_size: int = 100):
    os.makedirs(faiss_path, exist_ok=True)
    global index, metadata
    index = faiss.IndexFlatL2(384)
    metadata = []

    for i in range(0, len(clauses), batch_size):
        batch = clauses[i:i + batch_size]
        texts, sources = zip(*batch)
        vectors = model.encode(texts, show_progress_bar=False)
        index.add(vectors)
        metadata.extend(zip(texts, sources))

    save_vector_store()

def save_vector_store():
    faiss.write_index(index, index_file)
    with open(meta_file, "wb") as f:
        pickle.dump(metadata, f)

def search_similar_clauses(query: str, top_k: int = 5) -> List[str]:
    if index is None:
        initialize_vector_store()
    vector = model.encode([query])
    D, I = index.search(vector, top_k)
    return [metadata[i][0] for i in I[0] if i < len(metadata)]
