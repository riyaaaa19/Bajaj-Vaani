import os
import json
import faiss
from sentence_transformers import SentenceTransformer

# --- Constants ---
INDEX_DIR = "faiss_index"
FAISS_INDEX_PATH = os.path.join(INDEX_DIR, "index.faiss")
CLAUSES_JSON_PATH = os.path.join(INDEX_DIR, "clauses.json")

# --- Load Model Once ---
model = SentenceTransformer("all-MiniLM-L6-v2")

# --- Global Index and Metadata ---
index = None
metadata = None

# --- Load FAISS Index and Metadata Once ---
def load_index_once():
    global index, metadata
    if index and metadata:
        return
    print("📦 Loading FAISS index and metadata...")
    if not os.path.exists(FAISS_INDEX_PATH) or not os.path.exists(CLAUSES_JSON_PATH):
        raise FileNotFoundError("❌ FAISS index or metadata file missing.")
    index = faiss.read_index(FAISS_INDEX_PATH)
    with open(CLAUSES_JSON_PATH, "r", encoding="utf-8") as f:
        metadata = json.load(f)
    print(f"✅ Loaded {len(metadata)} clauses.")

# --- Search Clauses ---
def search_similar_clauses(query: str, top_k: int = 5) -> list[str]:
    load_index_once()
    query_vector = model.encode([query])
    distances, indices = index.search(query_vector, top_k)
    return [metadata[i]["text"] for i in indices[0] if i < len(metadata)]

# --- Add New Clauses ---
def add_clauses(new_clauses: list[str], source_file: str = "input"):
    if not new_clauses:
        print("⚠️ No clauses to add.")
        return
    load_index_once()
    vectors = model.encode(new_clauses)
    index.add(vectors)
    metadata.extend([{"text": clause, "source_file": source_file} for clause in new_clauses])
    _save_index_and_metadata()
    print(f"✅ Added {len(new_clauses)} new clauses.")

# --- Save Updated Index and Metadata ---
def _save_index_and_metadata():
    os.makedirs(INDEX_DIR, exist_ok=True)
    faiss.write_index(index, FAISS_INDEX_PATH)
    with open(CLAUSES_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)

# --- Build Index from Scratch ---
def build_initial_index(clauses: list[str]):
    if not clauses:
        print("⚠️ No input clauses.")
        return
    vectors = model.encode(clauses)
    new_index = faiss.IndexFlatL2(vectors.shape[1])
    new_index.add(vectors)
    os.makedirs(INDEX_DIR, exist_ok=True)
    faiss.write_index(new_index, FAISS_INDEX_PATH)
    with open(CLAUSES_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump([{"text": c, "source_file": "initial"} for c in clauses], f, indent=2)
    print(f"✅ Indexed {len(clauses)} initial clauses.")

# --- Clause Extractor (PDF/DOCX/EML) ---
def extract_clauses_from_file(file_path):
    from PyPDF2 import PdfReader
    from docx import Document
    from email import policy
    from email.parser import BytesParser

    ext = file_path.lower().split(".")[-1]
    text = ""

    try:
        if ext == "pdf":
            reader = PdfReader(file_path)
            text = "\n".join([p.extract_text() for p in reader.pages if p.extract_text()])
        elif ext == "docx":
            doc = Document(file_path)
            text = "\n".join([para.text for para in doc.paragraphs])
        elif ext == "eml":
            with open(file_path, "rb") as f:
                msg = BytesParser(policy=policy.default).parse(f)
                text = msg.get_body(preferencelist=('plain')).get_content()
        else:
            raise ValueError("Unsupported file format")
    except Exception as e:
        print(f"❌ Error reading file {file_path}: {e}")
        return []

    return [c.strip() for c in text.split("\n\n") if len(c.strip()) > 30]

# --- Load All Policy Documents from Folder ---
def load_all_policy_documents(folder_path="data/policy_docs"):
    all_clauses = []
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            try:
                clauses = extract_clauses_from_file(file_path)
                all_clauses.extend(clauses)
            except Exception as e:
                print(f"⚠️ Skipped {filename}: {e}")
    return all_clauses

# --- Debug: Show Current Index Clauses ---
def debug_print_indexed_clauses():
    load_index_once()
    print("\n📋 Indexed Clauses:\n")
    for i, item in enumerate(metadata):
        print(f"{i+1}. {item['text'][:100]}...\n")

# --- Main Entrypoint for Manual Indexing ---
if __name__ == "__main__":
    print("🔁 Building initial index from documents in 'data/policy_docs/' ...")
    clauses = load_all_policy_documents()
    if clauses:
        build_initial_index(clauses)
        debug_print_indexed_clauses()
    else:
        print("❌ No valid documents found.")
