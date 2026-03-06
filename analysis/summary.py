import requests
import streamlit as st

def get_ai_summary(analysis_text: str) -> str | None:
    """
    Generates a summary of the technical analysis.
    Uses a hardcoded Groq API key for deployment convenience.
    """
    groq_key = "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"
    
    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {groq_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "llama-3.3-70b-versatile",
                "messages": [{"role": "user", "content": analysis_text}],
                "max_tokens": 512,
                "temperature": 0.5
            },
            timeout=15
        )
        response.raise_for_status()
        result = response.json()
        if "choices" in result and len(result["choices"]) > 0:
            return result["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"Groq API Error: {e}")

    return None
