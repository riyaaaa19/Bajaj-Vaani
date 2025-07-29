import requests
import tempfile
import mimetypes
from PyPDF2 import PdfReader
from docx import Document

def fetch_and_save_document(url: str):
    response = requests.get(url)
    response.raise_for_status()
    ext = mimetypes.guess_extension(response.headers.get("Content-Type", "application/pdf"))
    with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
        tmp.write(response.content)
        return tmp.name

def extract_text_from_pdf(path: str):
    try:
        reader = PdfReader(path)
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    except Exception:
        return ""

def extract_text_from_docx(path: str):
    try:
        doc = Document(path)
        return "\n".join(paragraph.text for paragraph in doc.paragraphs)
    except Exception:
        return ""

def parse_document(path: str):
    if path.endswith(".pdf"):
        return extract_text_from_pdf(path)
    elif path.endswith(".docx"):
        return extract_text_from_docx(path)
    else:
        return ""
