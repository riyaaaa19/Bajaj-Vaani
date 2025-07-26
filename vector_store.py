from sentence_transformers import SentenceTransformer
import faiss
import json
import os

# --- Constants ---
FAISS_INDEX_PATH = "faiss_index/index.faiss"
CLAUSES_JSON_PATH = "faiss_index/clauses.json"

# --- Load Model ---
model = SentenceTransformer("all-MiniLM-L6-v2")

# --- Global Index and Metadata ---
index = None
metadata = None

# --- Index Loader ---
def load_index_once():
    global index, metadata
    if index is None or metadata is None:
        print("📦 Loading FAISS index and metadata...")
        if not os.path.exists(FAISS_INDEX_PATH):
            raise RuntimeError("❌ FAISS index missing. Run initial build.")
        index = faiss.read_index(FAISS_INDEX_PATH)
        with open(CLAUSES_JSON_PATH, "r", encoding="utf-8") as f:
            metadata = json.load(f)
        print(f"✅ Loaded {len(metadata)} clauses.")

# --- Search ---
def search_similar_clauses(query: str, top_k: int = 5) -> list[str]:
    load_index_once()
    query_vector = model.encode([query])
    distances, indices = index.search(query_vector, top_k)
    return [metadata[i]["text"] for i in indices[0] if i < len(metadata)]

# --- Add Clauses ---
def add_clauses(new_clauses: list[str], source_file: str = "input"):
    if not new_clauses:
        print("⚠️ No clauses to add.")
        return

    load_index_once()
    vectors = model.encode(new_clauses)
    index.add(vectors)

    for clause in new_clauses:
        metadata.append({
            "text": clause,
            "source_file": source_file
        })

    os.makedirs("faiss_index", exist_ok=True)
    faiss.write_index(index, FAISS_INDEX_PATH)
    with open(CLAUSES_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)

    print(f"✅ Added {len(new_clauses)} new clauses.")

# --- Build Initial Index ---
def build_initial_index(clauses: list[str]):
    if not clauses:
        print("⚠️ No input clauses.")
        return

    vectors = model.encode(clauses)
    faiss_index = faiss.IndexFlatL2(vectors.shape[1])
    faiss_index.add(vectors)

    os.makedirs("faiss_index", exist_ok=True)
    faiss.write_index(faiss_index, FAISS_INDEX_PATH)
    with open(CLAUSES_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump([{"text": c, "source_file": "initial"} for c in clauses], f, indent=2)

    print(f"✅ Indexed {len(clauses)} initial clauses.")

# --- Clause Extractor (PDF/DOCX/EML) ---
def extract_clauses_from_file(file_path):
    from PyPDF2 import PdfReader
    from docx import Document
    from email import policy
    from email.parser import BytesParser

    if file_path.endswith(".pdf"):
        reader = PdfReader(file_path)
        text = "\n".join([p.extract_text() for p in reader.pages if p.extract_text()])
    elif file_path.endswith(".docx"):
        doc = Document(file_path)
        text = "\n".join([para.text for para in doc.paragraphs])
    elif file_path.endswith(".eml"):
        with open(file_path, "rb") as f:
            msg = BytesParser(policy=policy.default).parse(f)
            text = msg.get_body(preferencelist=('plain')).get_content()
    else:
        raise ValueError("Unsupported file format")

    return [c.strip() for c in text.split("\n\n") if len(c.strip()) > 30]

# --- Load All Documents in Folder ---
def load_all_policy_documents(folder_path="data/policy_docs"):
    all_clauses = []
    for filename in os.listdir(folder_path):
        path = os.path.join(folder_path, filename)
        try:
            clauses = extract_clauses_from_file(path)
            for clause in clauses:
                all_clauses.append(clause)
        except Exception as e:
            print(f"⚠️ Skipped {filename}: {e}")
    return all_clauses

# --- Debug: Print All Indexed Clauses ---
def debug_print_indexed_clauses():
    load_index_once()
    print("\n📋 Indexed Clauses:\n")
    for i, item in enumerate(metadata):
        print(f"{i+1}. {item['text'][:100]}...\n")

# --- Main for Initial Indexing ---
if __name__ == "__main__":
    print("🔁 Building initial index from documents in 'data/policy_docs/' ...")
    clauses = load_all_policy_documents("data/policy_docs")
    if clauses:
        build_initial_index(clauses)
        debug_print_indexed_clauses()
    else:
        print("❌ No valid documents found.")