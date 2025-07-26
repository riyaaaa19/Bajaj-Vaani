import os
from PyPDF2 import PdfReader
from docx import Document
from email import policy
from email.parser import BytesParser

def extract_clauses_from_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        content = page.extract_text()
        if content:
            text += content + "\n"
    clauses = [clause.strip() for clause in text.split("\n\n") if len(clause.strip()) > 30]
    return clauses

def extract_clauses_from_docx(file_path):
    doc = Document(file_path)
    text = "\n".join([para.text for para in doc.paragraphs])
    clauses = [clause.strip() for clause in text.split("\n\n") if len(clause.strip()) > 30]
    return clauses

def extract_clauses_from_eml(file_path):
    try:
        with open(file_path, "rb") as f:
            msg = BytesParser(policy=policy.default).parse(f)
            body = msg.get_body(preferencelist=('plain'))
            if not body:
                return []
            text = body.get_content()
            clauses = [clause.strip() for clause in text.split("\n\n") if len(clause.strip()) > 30]
            return clauses
    except Exception as e:
        print(f"❌ Failed to parse EML: {file_path}, Error: {e}")
        return []

def extract_clauses_from_file(file_path):
    ext = file_path.lower().strip().split(".")[-1]
    if ext == "pdf":
        return extract_clauses_from_pdf(file_path)
    elif ext == "docx":
        return extract_clauses_from_docx(file_path)
    elif ext == "eml":
        return extract_clauses_from_eml(file_path)
    else:
        raise ValueError("Unsupported file format")

# Optional: remove if not indexing full directory
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
