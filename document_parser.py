import os
import re
import fitz  # PyMuPDF
import docx
import email
from bs4 import BeautifulSoup

def parse_pdf(path):
    text = ""
    try:
        with fitz.open(path) as doc:
            for page in doc:
                text += page.get_text()
    except Exception as e:
        print(f"[PDF ERROR] {path}: {e}")
    return text

def parse_docx(path):
    text = ""
    try:
        doc = docx.Document(path)
        text = "\n".join(p.text for p in doc.paragraphs if p.text.strip())
    except Exception as e:
        print(f"[DOCX ERROR] {path}: {e}")
    return text

def parse_eml(path):
    text = ""
    try:
        with open(path, "rb") as f:
            msg = email.message_from_binary_file(f)
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    text += part.get_payload(decode=True).decode(errors="ignore")
                elif part.get_content_type() == "text/html":
                    soup = BeautifulSoup(part.get_payload(decode=True), "html.parser")
                    text += soup.get_text()
    except Exception as e:
        print(f"[EML ERROR] {path}: {e}")
    return text

def extract_clauses(text):
    # Basic split on newlines and bullet points
    raw_clauses = re.split(r"\n+|(?<=\.)(?=\s+[A-Z0-9])|•", text)
    return [c.strip() for c in raw_clauses if len(c.strip()) > 30]

def parse_documents_from_path(paths):
    clauses = []
    seen = set()

    for path in paths:
        ext = os.path.splitext(path)[-1].lower()
        if ext == ".pdf":
            content = parse_pdf(path)
        elif ext == ".docx":
            content = parse_docx(path)
        elif ext == ".eml":
            content = parse_eml(path)
        else:
            continue

        for clause in extract_clauses(content):
            if clause not in seen:
                seen.add(clause)
                clauses.append(clause)

    return clauses
