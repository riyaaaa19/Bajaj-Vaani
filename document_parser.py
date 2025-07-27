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
    return [c.strip() for c in text.split("\n\n") if len(c.strip()) > 30]

def extract_clauses_from_docx(file_path):
    doc = Document(file_path)
    text = "\n".join([para.text for para in doc.paragraphs])
    return [c.strip() for c in text.split("\n\n") if len(c.strip()) > 30]

def extract_clauses_from_eml(file_path):
    try:
        with open(file_path, "rb") as f:
            msg = BytesParser(policy=policy.default).parse(f)
            body = msg.get_body(preferencelist=('plain'))
            if not body:
                return []
            text = body.get_content()
            return [c.strip() for c in text.split("\n\n") if len(c.strip()) > 30]
    except Exception as e:
        print(f"❌ Failed to parse EML: {file_path}, Error: {e}")
        return []
