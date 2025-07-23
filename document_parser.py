import os
from PyPDF2 import PdfReader
from docx import Document
import email
from email import policy
from email.parser import BytesParser

# Extract clauses from a PDF file
def extract_clauses_from_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        content = page.extract_text()
        if content:
            text += content + "\n"

    clauses = [clause.strip() for clause in text.split("\n\n") if len(clause.strip()) > 30]
    return clauses

# Extract clauses from a Word (.docx) file
def extract_clauses_from_docx(file_path):
    doc = Document(file_path)
    text = "\n".join([para.text for para in doc.paragraphs])
    clauses = [clause.strip() for clause in text.split("\n\n") if len(clause.strip()) > 30]
    return clauses

# Extract clauses from an email (.eml) file
def extract_clauses_from_eml(file_path):
    with open(file_path, "rb") as f:
        msg = BytesParser(policy=policy.default).parse(f)
        text = msg.get_body(preferencelist=('plain')).get_content()
        clauses = [clause.strip() for clause in text.split("\n\n") if len(clause.strip()) > 30]
        return clauses

# Master function to handle any file format
def extract_clauses_from_file(file_path):
    if file_path.endswith(".pdf"):
        return extract_clauses_from_pdf(file_path)
    elif file_path.endswith(".docx"):
        return extract_clauses_from_docx(file_path)
    elif file_path.endswith(".eml"):
        return extract_clauses_from_eml(file_path)
    else:
        raise ValueError("Unsupported file format")

# Optional: For batch indexing
def load_all_policy_documents(folder_path="data/policy_docs"):
    all_clauses = []
    for filename in os.listdir(folder_path):
        path = os.path.join(folder_path, filename)
        try:
            clauses = extract_clauses_from_file(path)
            for clause in clauses:
                all_clauses.append({
                    "text": clause,
                    "source_file": filename
                })
        except Exception as e:
            print(f"Skipping {filename}: {e}")
    return all_clauses
