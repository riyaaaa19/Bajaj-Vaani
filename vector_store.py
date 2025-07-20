import os
import faiss
import json
import numpy as np
from sentence_transformers import SentenceTransformer

CORPUS_PATH = "clauses.json"
INDEX_PATH = "index.faiss"
model = None  # Lazy-load model only when needed

def get_model():
    global model
    if model is None:
        print("🚀 Loading SentenceTransformer model...")
        model = SentenceTransformer('all-MiniLM-L6-v2')
    return model

# Load corpus from JSON
if os.path.exists(CORPUS_PATH):
    with open(CORPUS_PATH, "r", encoding="utf-8") as f:
        corpus = json.load(f)
else:
    corpus = []

# Load or initialize FAISS index
dim = 384  # for MiniLM model
index = faiss.IndexFlatL2(dim)
if os.path.exists(INDEX_PATH) and len(corpus) > 0:
    print("📂 Loading FAISS index...")
    embeddings = get_model().encode(corpus)
    index.add(np.array(embeddings))

# Save index + corpus
def save_to_disk():
    with open(CORPUS_PATH, "w", encoding="utf-8") as f:
        json.dump(corpus, f, ensure_ascii=False, indent=2)
    faiss.write_index(index, INDEX_PATH)

# Add new clauses
def add_clauses(new_clauses: list[str]):
    global corpus
    corpus.extend(new_clauses)
    new_embeddings = get_model().encode(new_clauses)
    index.add(np.array(new_embeddings))
    save_to_disk()

# Search relevant clauses
def search_similar_clauses(query, top_k=3):
    if len(corpus) == 0:
        return []
    query_vec = get_model().encode([query])
    D, I = index.search(query_vec, top_k)
    return [corpus[i] for i in I[0]]
