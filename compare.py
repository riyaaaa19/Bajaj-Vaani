from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")

def compare_policies(file1_clauses, file2_clauses, threshold=0.4, top_k=1):
    if not file1_clauses or not file2_clauses:
        return []

    embeddings1 = model.encode(file1_clauses)
    embeddings2 = model.encode(file2_clauses)

    similarity_matrix = cosine_similarity(embeddings1, embeddings2)

    results = []
    for i, row in enumerate(similarity_matrix):
        top_indices = row.argsort()[::-1][:top_k]
        for j in top_indices:
            score = row[j]
            if score >= threshold:
                results.append({
                    "clause_from_file1": file1_clauses[i],
                    "clause_from_file2": file2_clauses[j],
                    "similarity": float(round(score, 3))
                })

    return results
