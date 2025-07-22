# document_parser.py

import os
from PyPDF2 import PdfReader

def extract_clauses_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        content = page.extract_text()
        if content:
            text += content + "\n"

    # Loosen clause splitting condition to include shorter but meaningful clauses
    clauses = [clause.strip() for clause in text.split("\n\n") if len(clause.strip()) > 30]
    return clauses

def load_all_policy_documents(folder_path="data/policy_docs"):
    all_clauses = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            path = os.path.join(folder_path, filename)
            clauses = extract_clauses_from_pdf(path)
            for clause in clauses:
                all_clauses.append({
                    "text": clause,
                    "source_file": filename
                })
    return all_clauses
