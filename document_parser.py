import os
from PyPDF2 import PdfReader
from docx import Document
from email import policy
from email.parser import BytesParser
from bs4 import BeautifulSoup
from typing import List, Tuple

MIN_CLAUSE_LENGTH = 30

def extract_clauses_from_pdf(file_path):
    try:
        reader = PdfReader(file_path)
        text = "\n".join([p.extract_text() or "" for p in reader.pages])
        return [c.strip() for c in text.split("\n\n") if len(c.strip()) > MIN_CLAUSE_LENGTH]
    except Exception as e:
        print(f"❌ PDF parse failed: {e}")
        return []

def extract_clauses_from_docx(file_path):
    try:
        doc = Document(file_path)
        text = "\n".join(p.text for p in doc.paragraphs)
        return [c.strip() for c in text.split("\n\n") if len(c.strip()) > MIN_CLAUSE_LENGTH]
    except Exception as e:
        print(f"❌ DOCX parse failed: {e}")
        return []

def extract_clauses_from_eml(file_path):
    try:
        with open(file_path, "rb") as f:
            msg = BytesParser(policy=policy.default).parse(f)
            body = msg.get_body(preferencelist=('plain'))
            text = body.get_content() if body else ""
            return [c.strip() for c in text.split("\n\n") if len(c.strip()) > MIN_CLAUSE_LENGTH]
    except Exception as e:
        print(f"❌ EML parse failed: {e}")
        return []

def parse_documents_from_path(folder_path: str) -> List[Tuple[str, List[str]]]:
    all_clauses = []
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        suffix = filename.lower().split(".")[-1]

        if suffix == "pdf":
            clauses = extract_clauses_from_pdf(file_path)
        elif suffix == "docx":
            clauses = extract_clauses_from_docx(file_path)
        elif suffix == "eml":
            clauses = extract_clauses_from_eml(file_path)
        else:
            continue

        if clauses:
            all_clauses.append((filename, clauses))
    return all_clauses
