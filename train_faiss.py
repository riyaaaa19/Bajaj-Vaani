import os
import pickle
from document_parser import parse_documents_from_path
from vector_store import build_faiss_index

DOCUMENT_FOLDER = "data/policy_docs"
INDEX_OUTPUT_PATH = "faiss_index/index.pkl"

def collect_document_paths(folder):
    valid_exts = (".pdf", ".docx", ".eml")
    doc_paths = []
    for root, _, files in os.walk(folder):
        for file in files:
            if file.lower().endswith(valid_exts):
                doc_paths.append(os.path.join(root, file))
    return doc_paths

def main():
    doc_paths = collect_document_paths(DOCUMENT_FOLDER)
    if not doc_paths:
        print(f"No documents found in {DOCUMENT_FOLDER}")
        return

    print(f"Found {len(doc_paths)} documents. Parsing and indexing...")

    # Parse and split clauses
    all_clauses = parse_documents_from_path(doc_paths)

    # Build FAISS index
    index_data = build_faiss_index(all_clauses)

    # Save to disk
    os.makedirs(os.path.dirname(INDEX_OUTPUT_PATH), exist_ok=True)
    with open(INDEX_OUTPUT_PATH, "wb") as f:
        pickle.dump(index_data, f)

    print(f"✅ Index saved to {INDEX_OUTPUT_PATH} with {len(index_data['clauses'])} clauses.")

if __name__ == "__main__":
    main()
