import os
from document_parser import parse_documents_from_path
from vector_store import build_faiss_index

if __name__ == "__main__":
    folder_path = "data/policy_docs"
    if not os.path.exists(folder_path):
        raise FileNotFoundError("❌ 'data/policy_docs' folder not found.")

    all_documents = parse_documents_from_path(folder_path)
    build_faiss_index(all_documents)
    print("✅ FAISS index built successfully.")
