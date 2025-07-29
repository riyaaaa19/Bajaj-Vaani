import os
import requests
import tempfile
import fitz  # PyMuPDF
import docx
from PyPDF2 import PdfReader
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

embedder = SentenceTransformer("all-MiniLM-L6-v2")  # 80MB and fast

def extract_text_from_url(blob_url: str) -> str:
    response = requests.get(blob_url)
    response.raise_for_status()
    ext = blob_url.split(".")[-1].split("?")[0]
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{ext}") as tmp:
        tmp.write(response.content)
        tmp_path = tmp.name

    text = ""
    if ext == "pdf":
        reader = PdfReader(tmp_path)
        text = "\n".join(page.extract_text() for page in reader.pages if page.extract_text())
    elif ext == "docx":
        doc = docx.Document(tmp_path)
        text = "\n".join(p.text for p in doc.paragraphs if p.text.strip())
    elif ext == "eml":
        with open(tmp_path, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read()
    else:
        raise ValueError("Unsupported file type")

    os.unlink(tmp_path)
    return text

def split_into_clauses(text: str) -> List[str]:
    return [clause.strip() for clause in text.split("\n") if clause.strip()]

def index_documents(blob_url: str):
    text = extract_text_from_url(blob_url)
    clauses = split_into_clauses(text)

    embeddings = embedder.encode(clauses, convert_to_numpy=True)
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)

    return {
        "index": index,
        "clauses": clauses,
        "embeddings": embeddings
    }
