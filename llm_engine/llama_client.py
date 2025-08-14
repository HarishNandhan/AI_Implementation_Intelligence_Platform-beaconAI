import os
import logging
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

# Load environment variables from .env
load_dotenv("config/.env.example")

logger = logging.getLogger(__name__)

# Load Hugging Face credentials
HF_TOKEN = os.getenv("HF_TOKEN")
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "auto")
LLM_MODEL = os.getenv("LLM_MODEL", "mistralai/Mistral-7B-Instruct-v0.3")

# Validate token
if not HF_TOKEN:
    logger.error("❌ HF_TOKEN is not set in .env")
    raise ValueError("HF_TOKEN is required to access Hugging Face Inference API")

logger.info(f"✅ Using Hugging Face Model: {LLM_MODEL} via {LLM_PROVIDER}")

# Initialize Hugging Face InferenceClient
client = InferenceClient(provider=LLM_PROVIDER, api_key=HF_TOKEN)

def generate_llama_response(prompt: str) -> str:
    """
    Generates a strategic insight using a chat-compatible LLM (e.g., Mistral via HuggingFace).
    """
    try:
        response = client.chat.completions.create(
            model=LLM_MODEL,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=300
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        logger.error(f"❌ LLM call failed: {e}")

        # Custom user-friendly error messages
        if "401" in str(e) or "Unauthorized" in str(e):
            return "⚠️ Authentication failed. Check your Hugging Face token."
        elif "not supported for task" in str(e):
            return "⚠️ This model must be used as a chat model (chat.completions.create)."
        elif "404" in str(e):
            return f"⚠️ Model not found: {LLM_MODEL}. Double-check the model name."
        else:
            return f"⚠️ LLM call failed: {e}"
