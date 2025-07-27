import os
import json
import faiss
from sentence_transformers import SentenceTransformer

INDEX_DIR = "faiss_index"
FAISS_INDEX_PATH = os.path.join(INDEX_DIR, "index.faiss")
CLAUSES_JSON_PATH = os.path.join(INDEX_DIR, "clauses.json")

# --- Lazy Model Loader ---
def get_model():
    if not hasattr(get_model, "model"):
        get_model.model = SentenceTransformer("all-MiniLM-L6-v2")
    return get_model.model

# --- Load index & metadata only when needed ---
def load_index():
    if not os.path.exists(FAISS_INDEX_PATH) or not os.path.exists(CLAUSES_JSON_PATH):
        raise FileNotFoundError("❌ FAISS index or metadata missing.")
    index = faiss.read_index(FAISS_INDEX_PATH)
    with open(CLAUSES_JSON_PATH, "r", encoding="utf-8") as f:
        metadata = json.load(f)
    return index, metadata

def search_similar_clauses(query: str, top_k: int = 5) -> list[str]:
    index, metadata = load_index()
    model = get_model()
    query_vector = model.encode([query])
    distances, indices = index.search(query_vector, top_k)
    return [metadata[i]["text"] for i in indices[0] if i < len(metadata)]

def add_clauses(new_clauses: list[str], source_file: str = "input"):
    if not new_clauses:
        print("⚠️ No clauses to add.")
        return
    model = get_model()
    index, metadata = load_index()
    vectors = model.encode(new_clauses)
    index.add(vectors)
    metadata.extend([{"text": clause, "source_file": source_file} for clause in new_clauses])
    os.makedirs(INDEX_DIR, exist_ok=True)
    faiss.write_index(index, FAISS_INDEX_PATH)
    with open(CLAUSES_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)
    print(f"✅ Added {len(new_clauses)} new clauses.")
