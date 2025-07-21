import os
import faiss
import json
import numpy as np
from typing import List
from sentence_transformers import SentenceTransformer

# Constants
CORPUS_PATH = "clauses.json"
INDEX_PATH = "index.faiss"
DIM = 384  # Dimensionality for MiniLM

# Lazy-load model
model = None

def get_model():
    global model
    if model is None:
        print("🚀 Loading SentenceTransformer model...")
        model = SentenceTransformer("all-MiniLM-L6-v2")
    return model

# Load corpus
if os.path.exists(CORPUS_PATH):
    with open(CORPUS_PATH, "r", encoding="utf-8") as f:
        corpus = json.load(f)
else:
    corpus = []

# Load or create FAISS index
if os.path.exists(INDEX_PATH) and len(corpus) > 0:
    try:
        print("📂 Loading FAISS index...")
        index = faiss.read_index(INDEX_PATH)
    except Exception as e:
        print(f"⚠️ Failed to load FAISS index: {e}. Reinitializing.")
        index = faiss.IndexFlatL2(DIM)
else:
    index = faiss.IndexFlatL2(DIM)
    if len(corpus) > 0:
        embeddings = get_model().encode(corpus)
        index.add(np.array(embeddings))

# Save index and corpus
def save_to_disk():
    with open(CORPUS_PATH, "w", encoding="utf-8") as f:
        json.dump(corpus, f, ensure_ascii=False, indent=2)
    faiss.write_index(index, INDEX_PATH)

# Add new clauses to corpus and index
def add_clauses(new_clauses: List[str]):
    global corpus
    corpus.extend(new_clauses)
    embeddings = get_model().encode(new_clauses)
    index.add(np.array(embeddings))
    save_to_disk()

# Semantic search for similar clauses
def search_similar_clauses(query: str, top_k: int = 3) -> List[str]:
    if len(corpus) == 0:
        return []
    query_vec = get_model().encode([query])
    D, I = index.search(np.array(query_vec), top_k)
    return [corpus[i] for i in I[0]]
