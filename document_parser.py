import os
from typing import List, Tuple
from bs4 import BeautifulSoup
from PyPDF2 import PdfReader
import docx
import email

def extract_clauses_from_pdf(file_path: str) -> List[Tuple[str, str]]:
    reader = PdfReader(file_path)
    text = "\n".join(page.extract_text() or "" for page in reader.pages)
    return split_into_clauses(text), os.path.basename(file_path)

def extract_clauses_from_docx(file_path: str) -> List[Tuple[str, str]]:
    doc = docx.Document(file_path)
    text = "\n".join([p.text for p in doc.paragraphs])
    return split_into_clauses(text), os.path.basename(file_path)

def extract_clauses_from_eml(file_path: str) -> List[Tuple[str, str]]:
    with open(file_path, "r", encoding="utf-8") as f:
        msg = email.message_from_file(f)
        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    body += part.get_payload(decode=True).decode("utf-8", errors="ignore")
        else:
            body = msg.get_payload(decode=True).decode("utf-8", errors="ignore")
    soup = BeautifulSoup(body, "html.parser")
    text = soup.get_text()
    return split_into_clauses(text), os.path.basename(file_path)

def split_into_clauses(text: str) -> List[str]:
    return [c.strip() for c in text.split("\n") if len(c.strip()) > 30]

def parse_documents_from_folder(folder_path: str) -> List[Tuple[str, str]]:
    clauses = []
    for filename in os.listdir(folder_path):
        path = os.path.join(folder_path, filename)
        try:
            if filename.endswith(".pdf"):
                doc_clauses, src = extract_clauses_from_pdf(path)
            elif filename.endswith(".docx"):
                doc_clauses, src = extract_clauses_from_docx(path)
            elif filename.endswith(".eml"):
                doc_clauses, src = extract_clauses_from_eml(path)
            else:
                continue
            clauses.extend([(c, src) for c in doc_clauses])
        except Exception as e:
            print(f"⚠️ Error parsing {filename}: {e}")
    return clauses
