from query_agent import query_bajaj_vaani

def generate_response(query: str, clauses: list[str]) -> str:
    prompt = f"""You are an expert insurance assistant. Using the following policy clauses, answer the user query accurately and briefly.

User Query: {query}

Relevant Policy Clauses:
"""

    for idx, clause in enumerate(clauses, start=1):
        prompt += f"{idx}. {clause}\n"

    prompt += "\nGive a concise and fact-based answer based on the above clauses."

    return query_bajaj_vaani(prompt)
