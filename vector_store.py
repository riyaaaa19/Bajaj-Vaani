import os
import json
import faiss
from sentence_transformers import SentenceTransformer
from typing import List

INDEX_DIR = "faiss_index"
FAISS_INDEX_PATH = os.path.join(INDEX_DIR, "index.faiss")
CLAUSES_JSON_PATH = os.path.join(INDEX_DIR, "clauses.json")

model, index, metadata = None, None, []

def initialize_vector_store():
    global model, index, metadata
    model = SentenceTransformer("all-MiniLM-L6-v2")
    if os.path.exists(FAISS_INDEX_PATH) and os.path.exists(CLAUSES_JSON_PATH):
        index = faiss.read_index(FAISS_INDEX_PATH)
        with open(CLAUSES_JSON_PATH, "r", encoding="utf-8") as f:
            metadata = json.load(f)
    else:
        index = faiss.IndexFlatL2(model.get_sentence_embedding_dimension())
        metadata = []

def search_similar_clauses(query: str, top_k: int = 5) -> List[str]:
    global model, index, metadata
    if index is None or index.ntotal == 0:
        return []
    query_vector = model.encode([query])
    distances, indices = index.search(query_vector, top_k)
    return [metadata[i]["text"] for i in indices[0] if i < len(metadata)]

def add_clauses(new_clauses: List[str], source_file: str = "input"):
    global model, index, metadata
    if not new_clauses:
        return

    os.makedirs(INDEX_DIR, exist_ok=True)

    existing = set(m["text"] for m in metadata)
    unique_clauses = [c for c in new_clauses if c[:500] not in existing]
    if not unique_clauses:
        return

    vectors = model.encode(unique_clauses)
    index.add(vectors)

    metadata.extend([{"text": clause[:500], "source_file": source_file} for clause in unique_clauses])

    faiss.write_index(index, FAISS_INDEX_PATH)
    with open(CLAUSES_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)
