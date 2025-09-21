# auth.py

from fastapi import HTTPException

# Token as mentioned in the Problem Statement
HARDCODED_TEAM_TOKEN = "8c4bbc30a45570cc5b1e605cba9c98db4ca91fd254c9d612ebf43e051302194d"

def verify_token(token: str) -> str:
    if token != HARDCODED_TEAM_TOKEN:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return "team_user"
