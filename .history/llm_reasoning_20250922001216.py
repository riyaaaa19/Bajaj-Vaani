# llm_reasoning.py
import os
import re
from typing import Optional
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "").strip()
if not GOOGLE_API_KEY:
    raise RuntimeError("GOOGLE_API_KEY not set in environment variables")

# Configure Gemini API
genai.configure(api_key=GOOGLE_API_KEY)

# Initialize the model (Gemini 1.5 or Gemini Pro)
MODEL_NAME = "gemini-1.5-flash"
model = genai.GenerativeModel(MODEL_NAME)


# -------------------------
# Helper functions
# -------------------------
def clean_text(text: str) -> str:
    """
    Clean input text by removing extra spaces and line breaks.
    """
    return re.sub(r"\s+", " ", text).strip()


# -------------------------
# Answer a question
# -------------------------
def answer_question(question: str, conversation: Optional[genai.Chat] = None) -> str:
    """
    Answer a question using Gemini.
    If a conversation is provided, it continues the multi-turn chat.
    """
    question = clean_text(question)
    if not question:
        return "The question is empty."

    try:
        if conversation:
            # Multi-turn conversation
            response = conversation.send_message(question)
        else:
            # One-off prompt
            prompt = (
                "You are a helpful, friendly, and detailed AI assistant. "
                "Provide clear, easy-to-understand answers to the user's question.\n\n"
                f"Question: {question}\nAnswer:"
            )
            response = model.generate_content(prompt)

        # Gemini response text
        answer_text: Optional[str] = (response.text or "").strip()
        return answer_text or "No answer returned by Gemini."

    except Exception as e:
        return f"Error generating answer: {e}"


# -------------------------
# Start a conversation for document context
# -------------------------
def start_document_conversation(document_text: str) -> genai.Chat:
    """
    Initialize a conversation using document content as context.
    """
    document_text = clean_text(document_text)
    conversation = model.start_chat()
    conversation.send_message(
        f"You are a helpful assistant. Use the following document as context "
        f"for answering future questions:\n\n{document_text}"
    )
    return conversation
