from abc import ABC, abstractmethod
from google import genai
import requests


# Base class for all LLM providers
class LLMProvider(ABC):

    @abstractmethod
    def generate(self, prompt):
        pass


# Gemini API provider
class GeminiProvider(LLMProvider):

    def __init__(self, api_key):
        self.client = genai.Client(api_key=api_key)

    def generate(self, prompt):
        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return response.text


# Local Ollama provider
class OllamaProvider(LLMProvider):

    def __init__(self, model="llama3.2"):
        self.model = model
        self.url = "http://localhost:11434/api/generate"

    def generate(self, prompt):
        response = requests.post(
            self.url,
            json={
                "model": self.model,
                "prompt": prompt,
                "stream": False
            },
            timeout=120
        )

        response.raise_for_status()
        return response.json()["response"]


# Main client that works with any provider
class LLMClient:

    def __init__(self, provider):
        self.provider = provider

    def generate(self, prompt):
        return self.provider.generate(prompt)