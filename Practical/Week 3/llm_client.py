
import os
import time
import requests

from dotenv import load_dotenv
from google import genai

load_dotenv()

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")
GEMINI_MODEL = "gemini-2.5-flash"


def generate_with_ollama(prompt):
    """Generate a response using local Ollama."""

    start_time = time.time()

    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(
        OLLAMA_URL,
        json=payload,
        timeout=180
    )

    response.raise_for_status()
    data = response.json()

    return {
        "provider": "ollama",
        "model": OLLAMA_MODEL,
        "response": data["response"],
        "input_tokens": data.get("prompt_eval_count", 0),
        "output_tokens": data.get("eval_count", 0),
        "response_time": round(time.time() - start_time, 3)
    }


def generate_with_gemini(prompt):
    """Generate a response using Google Gemini."""

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError("GEMINI_API_KEY is missing in .env")

    client = genai.Client(api_key=api_key)

    start_time = time.time()

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt
    )

    response_time = round(time.time() - start_time, 3)

    usage = response.usage_metadata

    return {
        "provider": "gemini",
        "model": GEMINI_MODEL,
        "response": response.text,
        "input_tokens": usage.prompt_token_count if usage else 0,
        "output_tokens": usage.candidates_token_count if usage else 0,
        "response_time": response_time
    }


def generate_response(prompt, provider="ollama"):
    """Common interface for both LLM providers."""

    if provider.lower() == "ollama":
        return generate_with_ollama(prompt)

    elif provider.lower() == "gemini":
        return generate_with_gemini(prompt)

    else:
        raise ValueError(
            "Invalid provider. Choose 'ollama' or 'gemini'."
        )
