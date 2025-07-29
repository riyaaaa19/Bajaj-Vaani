from PyPDF2 import PdfReader
from docx import Document
from email import policy
from email.parser import BytesParser

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
            if not body:
                return []
            text = body.get_content()
            return [c.strip() for c in text.split("\n\n") if len(c.strip()) > MIN_CLAUSE_LENGTH]
    except Exception as e:
        print(f"❌ EML parse failed: {e}")
        return []
