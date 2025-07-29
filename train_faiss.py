import os
import pickle
import faiss
from sentence_transformers import SentenceTransformer
from vector_store import get_clause_chunks

INDEX_FILE = "index/faiss.index"
METADATA_FILE = "index/metadata.pkl"
MODEL = SentenceTransformer("all-MiniLM-L6-v2")

def build_faiss_index(texts):
    embeddings = MODEL.encode(texts, convert_to_tensor=False)
    index = faiss.IndexFlatL2(len(embeddings[0]))
    index.add(embeddings)
    return index, embeddings

def train_faiss_from_documents(documents):
    all_clauses = get_clause_chunks(documents)
    texts = list(set([c["text"] for c in all_clauses]))  # deduplicated
    index, _ = build_faiss_index(texts)

    os.makedirs("index", exist_ok=True)
    faiss.write_index(index, INDEX_FILE)
    with open(METADATA_FILE, "wb") as f:
        pickle.dump(texts, f)
    return len(texts)
