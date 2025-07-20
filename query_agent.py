import os
from dotenv import load_dotenv
from omnidimension import Client

load_dotenv()

api_key = os.getenv("OMNIDIMENSION_API_KEY")
agent_id = os.getenv("OMNI_AGENT_ID", "5718")  # Your real agent ID here

client = Client(api_key)

def query_bajaj_vaani(user_input: str):
    response = client.call.create(agent_id=agent_id, message=user_input)
    return response["json"].get("response", "No reply from agent.")
