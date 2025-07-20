from query_agent import query_bajaj_vaani

def generate_response(query, matches):
    prompt = f"""
User Query: {query}
Matched Clauses: {matches}

Based on the clauses, provide:
- A decision (Covered/Not Covered)
- A short explanation
- Any relevant conditions
"""
    return query_bajaj_vaani(prompt)
