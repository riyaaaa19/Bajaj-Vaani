# llm_reasoning.py

from query_agent import query_bajaj_vaani

def generate_response(query, matches):
    prompt = f"""
You are an intelligent insurance assistant.

User Query:
{query}

Relevant Policy Clauses:
{matches}

Task:
- Determine if the user's case is covered or not.
- Give a short justification.
- Refer to the most relevant clauses in your reasoning.

Respond in this exact JSON format:
{{
  "decision": "Covered" or "Not Covered",
  "justification": "<short explanation>",
  "referenced_clauses": ["clause excerpt 1", "clause excerpt 2"]
}}
"""
    return query_bajaj_vaani(prompt)
