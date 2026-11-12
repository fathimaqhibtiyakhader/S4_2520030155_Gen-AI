
import os

from dotenv import load_dotenv

from llm_client import generate_response
from cost_calculator import calculate_cost
from mongo_logger import log_call

load_dotenv()


def main():

    print("\n===================================")
    print("       LLM MONITORING SYSTEM")
    print("===================================\n")

    provider = os.getenv(
        "DEFAULT_PROVIDER", "ollama"
    ).lower()

    print("Available providers:")
    print("1. Ollama (Local Llama 3.2)")
    print("2. Gemini (Google API)")

    choice = input("\nChoose provider (1 or 2): ").strip()

    if choice == "1":
        provider = "ollama"
    elif choice == "2":
        provider = "gemini"
    elif choice == "":
        print("Using default provider:", provider)
    else:
        print("Invalid choice!")
        return

    prompt = input("\nEnter your prompt: ").strip()

    if not prompt:
        print("Prompt cannot be empty!")
        return

    try:
        print("\nGenerating response...\n")

        result = generate_response(
            prompt,
            provider=provider
        )

        # Local Ollama inference has no API token charge.
        if provider == "ollama":
            input_price = 0
            output_price = 0
        else:
            # Configure these rates in .env using
            # the official model pricing per million tokens.
            input_price = float(
                os.getenv("GEMINI_INPUT_PRICE_PER_MILLION", "0")
            )
            output_price = float(
                os.getenv("GEMINI_OUTPUT_PRICE_PER_MILLION", "0")
            )

        cost_data = calculate_cost(
            result["input_tokens"],
            result["output_tokens"],
            input_price,
            output_price
        )

        print("========== AI RESPONSE ==========")
        print(result["response"])

        print("\n========== MONITORING DETAILS ==========")
        print("Provider:", result["provider"])
        print("Model:", result["model"])
        print("Input tokens:", result["input_tokens"])
        print("Output tokens:", result["output_tokens"])
        print("Response time:", result["response_time"], "seconds")
        print("Estimated cost:", cost_data["total_cost"])

        log_data = {
            **result,
            "prompt": prompt,
            "cost": cost_data["total_cost"]
        }

        print("\nSaving interaction to MongoDB...")

        log_call(log_data)

        print("\n========== EXECUTION COMPLETE ==========")

    except Exception as error:
        print("\nAn error occurred:", error)


if __name__ == "__main__":
    main()
