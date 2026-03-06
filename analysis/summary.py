import requests
import streamlit as st

def get_ai_summary(analysis_text: str) -> str | None:
    """
    Generates a summary of the technical analysis.
    Tries Groq (llama-3.3-70b-versatile) first, falls back to Hugging Face.
    """
    # 1. Try Groq
    groq_key = st.secrets.get("GROQ_API_KEY")
    if groq_key:
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

    # 2. Fallback to Hugging Face
    hf_key = st.secrets.get("HF_API_KEY")
    if hf_key:
        try:
            response = requests.post(
                "https://router.huggingface.co/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {hf_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "Qwen/Qwen2.5-72B-Instruct",
                    "messages": [{"role": "user", "content": analysis_text}],
                    "max_tokens": 500
                },
                timeout=20
            )
            response.raise_for_status()
            result = response.json()
            if "choices" in result and len(result["choices"]) > 0:
                return result["choices"][0]["message"]["content"]
        except Exception as e:
            print(f"Hugging Face API Fallback Error: {e}")

    return None
