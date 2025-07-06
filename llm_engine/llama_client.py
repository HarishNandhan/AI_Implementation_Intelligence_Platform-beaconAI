import os
import httpx
from dotenv import load_dotenv

# Load API keys from .env
load_dotenv()
LLM_API_URL = os.getenv("LLM_API_URL")  # e.g., "https://your-llm-host.com/generate"
LLM_API_KEY = os.getenv("LLM_API_KEY")  # Optional if using auth

def generate_llama_response(prompt: str) -> str:
    """
    Sends prompt to LLAMA API and returns the generated text.
    """

    try:
        headers = {
            "Content-Type": "application/json"
        }
        if LLM_API_KEY:
            headers["Authorization"] = f"Bearer {LLM_API_KEY}"

        payload = {
            "prompt": prompt,
            "max_tokens": 300,
            "temperature": 0.7,
        }

        response = httpx.post(LLM_API_URL, headers=headers, json=payload)
        response.raise_for_status()

        result = response.json()

        # Adjust this depending on how your LLM API formats output
        insight = result.get("text") or result.get("response") or result.get("choices", [{}])[0].get("text")

        if not insight:
            raise ValueError("No text returned from LLM.")

        return insight.strip()

    except Exception as e:
        return f"⚠️ LLM generation failed: {e}"
