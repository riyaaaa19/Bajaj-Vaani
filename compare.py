from sentence_transformers import SentenceTransformer
from PyPDF2 import PdfReader
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")

def extract_clauses(pdf_file):
    reader = PdfReader(pdf_file)
    full_text = ""

    for page in reader.pages:
        content = page.extract_text()
        if content:
            full_text += content + "\n"

    clauses = [clause.strip() for clause in full_text.split("\n\n") if len(clause.strip()) > 30]
    return clauses

def compare_policies(file1_stream, file2_stream, threshold=0.4, top_k=1):
    clauses1 = extract_clauses(file1_stream)
    clauses2 = extract_clauses(file2_stream)

    if not clauses1 or not clauses2:
        return []

    embeddings1 = model.encode(clauses1)
    embeddings2 = model.encode(clauses2)

    similarity_matrix = cosine_similarity(embeddings1, embeddings2)

    results = []
    for i, row in enumerate(similarity_matrix):
        # Get top_k matches (indices and scores)
        top_indices = row.argsort()[::-1][:top_k]
        for j in top_indices:
            score = row[j]
            if score >= threshold:
                results.append({
                    "clause_from_file1": clauses1[i],
                    "clause_from_file2": clauses2[j],
                    "similarity": float(round(score, 3))
                })

    return results
