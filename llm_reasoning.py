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
- Look for exclusions, waiting periods (e.g., 30 days), and policy duration limits.
- If the policy duration is too short to pass the waiting period, respond "Not Covered".
- Give a short, factual justification.
- Refer to specific clauses supporting your decision.

Respond strictly in this JSON format:
{{
  "decision": "Covered" or "Not Covered",
  "justification": "<brief explanation>",
  "referenced_clauses": ["clause excerpt 1", "clause excerpt 2"]
}}
"""
    return query_bajaj_vaani(prompt)
