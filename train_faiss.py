import os
from document_parser import parse_documents_from_folder
from vector_store import build_faiss_index

if __name__ == "__main__":
    folder_path = "data/policy_docs"
    if not os.path.exists(folder_path):
        print(f"❌ Folder not found: {folder_path}")
        exit(1)

    print("📂 Parsing documents...")
    all_clauses = parse_documents_from_folder(folder_path)
    print(f"✅ Total clauses extracted: {len(all_clauses)}")

    print("🧠 Building FAISS index in batches...")
    build_faiss_index(all_clauses, batch_size=100)
    print("🎉 FAISS index build complete.")
