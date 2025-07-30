import requests
import fitz  # PyMuPDF
import mimetypes
import tempfile
from bs4 import BeautifulSoup
from docx import Document
import email

def parse_documents_from_url(url: str) -> str:
    response = requests.get(url)
    content_type = response.headers.get("Content-Type")
    ext = mimetypes.guess_extension(content_type or "")

    with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
        tmp.write(response.content)
        tmp.flush()
        if ext == ".pdf":
            return extract_text_from_pdf(tmp.name)
        elif ext == ".docx":
            return extract_text_from_docx(tmp.name)
        elif ext == ".eml":
            return extract_text_from_eml(tmp.name)
        else:
            raise Exception("Unsupported file type")

def extract_text_from_pdf(path: str) -> str:
    text = ""
    with fitz.open(path) as doc:
        for page in doc:
            text += page.get_text()
    return text

def extract_text_from_docx(path: str) -> str:
    doc = Document(path)
    return "\n".join([para.text for para in doc.paragraphs])

def extract_text_from_eml(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        msg = email.message_from_file(f)
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/html":
                    return BeautifulSoup(part.get_payload(decode=True), "html.parser").get_text()
        else:
            return msg.get_payload()
    return ""
