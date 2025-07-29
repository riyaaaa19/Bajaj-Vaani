import os
import json
import faiss
from typing import List, Tuple
from sentence_transformers import SentenceTransformer

INDEX_DIR = "faiss_index"
FAISS_INDEX_PATH = os.path.join(INDEX_DIR, "index.faiss")
CLAUSES_JSON_PATH = os.path.join(INDEX_DIR, "clauses.json")

model = SentenceTransformer("all-MiniLM-L6-v2")
index = None
metadata = []

def initialize_vector_store():
    global index, metadata
    if os.path.exists(FAISS_INDEX_PATH) and os.path.exists(CLAUSES_JSON_PATH):
        index = faiss.read_index(FAISS_INDEX_PATH)
        with open(CLAUSES_JSON_PATH, "r", encoding="utf-8") as f:
            metadata = json.load(f)
    else:
        index = faiss.IndexFlatL2(model.get_sentence_embedding_dimension())
        metadata = []

def search_similar_clauses(query: str, top_k: int = 5) -> List[str]:
    if index is None or index.ntotal == 0:
        return []
    query_vector = model.encode([query])
    distances, indices = index.search(query_vector, top_k)
    return [metadata[i]["text"] for i in indices[0] if i < len(metadata)]

def add_clauses(new_clauses: List[str], source_file: str = "input"):
    global index, metadata
    os.makedirs(INDEX_DIR, exist_ok=True)

    existing_texts = set(m["text"] for m in metadata)
    unique_clauses = [c.strip()[:500] for c in new_clauses if c.strip()[:500] not in existing_texts]

    if not unique_clauses:
        return

    vectors = model.encode(unique_clauses)
    index.add(vectors)

    new_meta = [{"text": clause, "source_file": source_file} for clause in unique_clauses]
    metadata.extend(new_meta)

    faiss.write_index(index, FAISS_INDEX_PATH)
    with open(CLAUSES_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)

def build_faiss_index(all_documents: List[Tuple[str, List[str]]]):
    global index, metadata
    index = faiss.IndexFlatL2(model.get_sentence_embedding_dimension())
    metadata = []

    for filename, clauses in all_documents:
        vectors = model.encode([c[:500] for c in clauses])
        index.add(vectors)
        metadata.extend([{"text": c[:500], "source_file": filename} for c in clauses])

    os.makedirs(INDEX_DIR, exist_ok=True)
    faiss.write_index(index, FAISS_INDEX_PATH)
    with open(CLAUSES_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)
