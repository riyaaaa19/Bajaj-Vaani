import os
import json
import faiss
from sentence_transformers import SentenceTransformer
import logging

INDEX_DIR = "faiss_index"
FAISS_INDEX_PATH = os.path.join(INDEX_DIR, "index.faiss")
CLAUSES_JSON_PATH = os.path.join(INDEX_DIR, "clauses.json")

model, index, metadata = None, None, []

def initialize_vector_store():
    global model, index, metadata
    logging.info("🔁 Initializing FAISS and SentenceTransformer...")
    model = SentenceTransformer("all-MiniLM-L6-v2")

    if os.path.exists(FAISS_INDEX_PATH) and os.path.exists(CLAUSES_JSON_PATH):
        index = faiss.read_index(FAISS_INDEX_PATH)
        with open(CLAUSES_JSON_PATH, "r", encoding="utf-8") as f:
            metadata = json.load(f)
        logging.info("✅ Loaded FAISS index and metadata")
    else:
        index = faiss.IndexFlatL2(model.get_sentence_embedding_dimension())
        metadata = []
        logging.info("🆕 Created new FAISS index")

def search_similar_clauses(query: str, top_k: int = 5) -> list[str]:
    global model, index, metadata
    if index is None or index.ntotal == 0:
        return []
    query_vector = model.encode([query])
    distances, indices = index.search(query_vector, top_k)
    return [metadata[i]["text"] for i in indices[0] if i < len(metadata)]

def add_clauses(new_clauses: list[str], source_file: str = "input"):
    global model, index, metadata
    if not new_clauses:
        logging.warning("⚠️ No clauses to add.")
        return

    vectors = model.encode(new_clauses)
    index.add(vectors)

    new_meta = [
        {"text": clause[:500], "source_file": source_file}
        for clause in new_clauses
    ]
    metadata.extend(new_meta)

    os.makedirs(INDEX_DIR, exist_ok=True)
    faiss.write_index(index, FAISS_INDEX_PATH)
    with open(CLAUSES_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)

    logging.info(f"✅ Added {len(new_clauses)} new clauses from {source_file}")
