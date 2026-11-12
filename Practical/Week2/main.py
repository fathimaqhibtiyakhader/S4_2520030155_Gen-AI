import os
from dotenv import load_dotenv

from llm_client import GeminiProvider, OllamaProvider, LLMClient

load_dotenv(override=True)

print("Choose your LLM provider:")
print("1. Gemini (Cloud API)")
print("2. Ollama (Local LLM)")

choice = input("Enter 1 or 2: ").strip()

if choice == "1":
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        print("Error: GEMINI_API_KEY not found in .env")
        exit()

    provider = GeminiProvider(api_key)

elif choice == "2":
    provider = OllamaProvider()

else:
    print("Invalid choice!")
    exit()

client = LLMClient(provider)

prompt = input("\nEnter your prompt: ")

try:
    answer = client.generate(prompt)
    print("\nLLM Response:")
    print(answer)

except Exception as e:
    print("\nError:", e)