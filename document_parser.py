import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extracts and returns the full text content from a PDF file.

    Args:
        pdf_path (str): The file path to the PDF document.

    Returns:
        str: Concatenated text from all pages.
    """
    try:
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        return text
    except Exception as e:
        print(f"❌ Error while extracting text: {e}")
        return ""
