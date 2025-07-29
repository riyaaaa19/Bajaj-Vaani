import os
from document_parser import extract_clauses_from_pdf
from vector_store import initialize_vector_store, add_clauses

POLICY_DIR = "data/policy_docs"

def train_faiss():
    if not os.path.exists(POLICY_DIR):
        print(f"❌ Directory not found: {POLICY_DIR}")
        return

    initialize_vector_store()

    total = 0
    for file in os.listdir(POLICY_DIR):
        if file.endswith(".pdf"):
            path = os.path.join(POLICY_DIR, file)
            print(f"📄 Processing {file}...")
            try:
                clauses = extract_clauses_from_pdf(path)
                print(f"   🔹 Found {len(clauses)} clauses")
                add_clauses(clauses, source_file=file)
                total += len(clauses)
            except Exception as e:
                print(f"   ❌ Failed to process {file}: {e}")

    print(f"\n✅ Done. Total indexed clauses: {total}")

if __name__ == "__main__":
    train_faiss()
