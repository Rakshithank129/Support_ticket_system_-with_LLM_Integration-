import os
import json
from openai import OpenAI
from ticketsapp.models import Ticket  

def classify_ticket(description):
    api_key = os.getenv("OPENAI_API_KEY")

    # If no API key, disable LLM cleanly
    if not api_key:
        print("LLM disabled: No API key provided")
        return {
            "suggested_category": None,
            "suggested_priority": None
        }

    try:
        client = OpenAI(
            api_key=api_key,
            timeout=10  # prevents hanging
        )

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You classify support tickets."
                },
                {
                    "role": "user",
                    "content": f"""Classify this support ticket.
                    Categories:Billing,Technical,Account,General
                    Priorities:Low,Medium,High
                    Return ONLY valid JSON like:{{"suggested_category":"Billing","suggested_priority":"High"}}
                    Ticket:{description}"""
                }       
            ],temperature=0)
                
        content = response.choices[0].message.content.strip()

        if content.startswith("```"):
            content = content.replace("```json", "").replace("```", "").strip()

        parsed = json.loads(content)

        return {
    "suggested_category": parsed.get("suggested_category", "").lower() or None,
    "suggested_priority": parsed.get("suggested_priority", "").lower() or None,
}
    except Exception as e:
        print(f"LLM classification error: {e}")
        return {
            "suggested_category": None,
            "suggested_priority": None
        }   
