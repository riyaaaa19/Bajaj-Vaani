import os
import json
import faiss
from sentence_transformers import SentenceTransformer

# --- Constants ---
INDEX_DIR = "faiss_index"
FAISS_INDEX_PATH = os.path.join(INDEX_DIR, "index.faiss")
CLAUSES_JSON_PATH = os.path.join(INDEX_DIR, "clauses.json")

# --- Global In-Memory Variables ---
model = None
index = None
metadata = None

# --- Load on Startup ---
def initialize_vector_store():
    global model, index, metadata

    print("🔁 Initializing model and FAISS index...")

    # Load model once
    model = SentenceTransformer("all-MiniLM-L6-v2")

    # Load FAISS index
    if not os.path.exists(FAISS_INDEX_PATH) or not os.path.exists(CLAUSES_JSON_PATH):
        raise FileNotFoundError("❌ FAISS index or metadata missing.")
    index = faiss.read_index(FAISS_INDEX_PATH)
    with open(CLAUSES_JSON_PATH, "r", encoding="utf-8") as f:
        metadata = json.load(f)

    print("✅ Model and FAISS index loaded into memory.")


# --- Semantic Search ---
def search_similar_clauses(query: str, top_k: int = 5) -> list[str]:
    global model, index, metadata
    query_vector = model.encode([query])
    distances, indices = index.search(query_vector, top_k)
    return [metadata[i]["text"] for i in indices[0] if i < len(metadata)]


# --- Add Clauses ---
def add_clauses(new_clauses: list[str], source_file: str = "input"):
    global model, index, metadata

    if not new_clauses:
        print("⚠️ No clauses to add.")
        return

    vectors = model.encode(new_clauses)
    index.add(vectors)
    metadata.extend([{"text": clause, "source_file": source_file} for clause in new_clauses])

    # Save changes
    os.makedirs(INDEX_DIR, exist_ok=True)
    faiss.write_index(index, FAISS_INDEX_PATH)
    with open(CLAUSES_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)

    print(f"✅ Added {len(new_clauses)} new clauses.")
