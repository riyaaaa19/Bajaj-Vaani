from document_parser import load_all_policy_documents, extract_clauses_from_file
from sentence_transformers import SentenceTransformer
import faiss
import json
import os

FAISS_INDEX_PATH = "faiss_index/index.faiss"
CLAUSES_JSON_PATH = "faiss_index/clauses.json"

# Use SentenceTransformer model
model = SentenceTransformer("all-MiniLM-L6-v2")

def build_faiss_index():
    clauses = load_all_policy_documents("data/policy_docs")
    if not clauses:
        print("⚠️ No valid documents or clauses found.")
        return

    texts = [c["text"] for c in clauses]
    vectors = model.encode(texts)

    index = faiss.IndexFlatL2(vectors.shape[1])
    index.add(vectors)

    os.makedirs("faiss_index", exist_ok=True)
    faiss.write_index(index, FAISS_INDEX_PATH)
    with open(CLAUSES_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(clauses, f, ensure_ascii=False, indent=2)

    print(f"✅ Indexed {len(clauses)} clauses from policy documents.")

def load_faiss_and_metadata():
    if not os.path.exists(FAISS_INDEX_PATH):
        raise RuntimeError("❌ FAISS index not found. Run vector_store.py to generate it.")
    index = faiss.read_index(FAISS_INDEX_PATH)
    with open(CLAUSES_JSON_PATH, "r", encoding="utf-8") as f:
        metadata = json.load(f)
    return index, metadata

def search_similar_clauses(query, top_k=5):
    index, metadata = load_faiss_and_metadata()
    query_vector = model.encode([query])
    distances, indices = index.search(query_vector, top_k)
    results = [metadata[i]["text"] for i in indices[0] if i < len(metadata)]
    return results

def add_clauses(new_clauses, source_file="uploaded_file"):
    try:
        index, metadata = load_faiss_and_metadata()
    except Exception:
        index = faiss.IndexFlatL2(model.get_sentence_embedding_dimension())
        metadata = []

    new_vectors = model.encode(new_clauses)
    index.add(new_vectors)

    for clause in new_clauses:
        metadata.append({
            "text": clause,
            "source_file": source_file
        })

    os.makedirs("faiss_index", exist_ok=True)
    faiss.write_index(index, FAISS_INDEX_PATH)
    with open(CLAUSES_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)

    print(f"✅ Added {len(new_clauses)} new clauses to index.")

if __name__ == "__main__":
    build_faiss_index()
