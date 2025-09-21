# document_parser.py
import requests
import tempfile
import os
import fitz  # PyMuPDF
import docx
from bs4 import BeautifulSoup
from typing import cast

def parse_documents_from_url(url: str) -> str:
    """
    Download the document from the given URL and extract its text.
    Supports PDF, DOCX, HTML/EML, TXT.
    """
    # Stream download to avoid memory overload
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        r = requests.get(url, stream=True, timeout=20)
        r.raise_for_status()
        for chunk in r.iter_content(chunk_size=8192):
            tmp.write(chunk)
        tmp_path = tmp.name

    try:
        if url.lower().endswith(".pdf"):
            text = extract_text_from_pdf(tmp_path)
        elif url.lower().endswith(".docx"):
            text = extract_text_from_docx(tmp_path)
        elif url.lower().endswith(".eml") or url.lower().endswith(".html"):
            text = extract_text_from_html(tmp_path)
        else:
            text = read_as_text(tmp_path)
    finally:
        os.remove(tmp_path)

    return text.strip()


def extract_text_from_pdf(path: str) -> str:
    """Extract text from PDF using PyMuPDF."""
    import fitz  # local import to avoid type issues

    text_chunks = []
    with fitz.open(path) as pdf:
        for page in pdf:
            # Tell Pylance this has get_text
            page = cast(fitz.Page, page)
            text_chunks.append(page.get_text("text"))  # type: ignore[attr-defined]
    return "\n".join(filter(None, text_chunks))


def extract_text_from_docx(path: str) -> str:
    """Extract text from DOCX file."""
    text_chunks = []
    doc = docx.Document(path)
    for para in doc.paragraphs:
        if para.text.strip():
            text_chunks.append(para.text)
    return "\n".join(text_chunks)


def extract_text_from_html(path: str) -> str:
    """Extract text from HTML/EML using BeautifulSoup."""
    with open(path, "rb") as f:
        soup = BeautifulSoup(f.read(), "html.parser")
    return soup.get_text(separator="\n")


def read_as_text(path: str) -> str:
    """Fallback for plain text files."""
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()
