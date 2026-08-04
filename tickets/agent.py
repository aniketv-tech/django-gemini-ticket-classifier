import os
import json
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Dynamically locate project root and load .env from either root or core folder
BASE_DIR = Path(__file__).resolve().parent.parent
env_path = BASE_DIR / "core" / ".env" if (BASE_DIR / "core" / ".env").exists() else BASE_DIR / ".env"
load_dotenv(dotenv_path=env_path)

def classify_and_draft_agent(ticket_text: str) -> dict:
    api_key = os.getenv("GEMINI_API_KEY")
    
    print("----------------------------------------")
    print("DEBUG API KEY READ:", api_key)
    print("----------------------------------------")

    # Guardrail 1: If no API key is found, fall back to offline rules instantly
    if not api_key:
        print("DEBUG: API key not found! Falling back to offline logic.")
        return _fallback_local_agent(ticket_text)

    try:
        client = genai.Client(api_key=api_key)

        prompt = f"""
        You are a pirate AI customer support agent. Analyze the following support ticket message:
        "{ticket_text}"

        Respond strictly in valid JSON format with three keys:
        1. "category": Choose one from ["Billing", "Technical Support", "Feature Request", "General Inquiry"]
        2. "priority": Choose one from ["High", "Medium", "Low"]
        3. "auto_reply": A pirate-style resolution reply starting with "Ahoy matey!".
        """

        # Guardrail 2: Standard Flash model for Google GenAI SDK
        response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                temperature=0.3
            )
        )

        return json.loads(response.text)

    except Exception as e:
        print("\nGEMINI ERROR:", str(e), "\n")
        return _fallback_local_agent(ticket_text)


def _fallback_local_agent(ticket_text: str) -> dict:
    """Backup offline logic so your server never crashes."""
    text_lower = ticket_text.lower()

    if any(k in text_lower for k in ["payment", "charge", "refund", "billing", "invoice"]):
        return {
            "category": "Billing",
            "priority": "High",
            "auto_reply": "Hello, thanks for reaching out. We have logged your billing inquiry with our finance team."
        }
    elif any(k in text_lower for k in ["error", "bug", "crash", "broken", "fail"]):
        return {
            "category": "Technical Support",
            "priority": "High",
            "auto_reply": "Hi there! Our engineering team has been notified of this technical issue."
        }
    else:
        return {
            "category": "General Inquiry",
            "priority": "Low",
            "auto_reply": "Hello! A customer support representative will get back to you shortly."
        }