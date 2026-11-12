
def calculate_cost(
    input_tokens,
    output_tokens,
    input_price_per_million,
    output_price_per_million
):
    """
    Calculate the estimated cost of an LLM API call.

    Prices are supplied in currency units per million tokens.
    """

    input_cost = (
        input_tokens / 1_000_000
    ) * input_price_per_million

    output_cost = (
        output_tokens / 1_000_000
    ) * output_price_per_million

    total_cost = input_cost + output_cost

    return {
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "input_cost": round(input_cost, 8),
        "output_cost": round(output_cost, 8),
        "total_cost": round(total_cost, 8)
    }


if __name__ == "__main__":
    result = calculate_cost(
        input_tokens=1000,
        output_tokens=500,
        input_price_per_million=0.50,
        output_price_per_million=1.50
    )

    print("LLM Cost Calculation")
    print("--------------------")
    print(f"Input tokens: {result['input_tokens']}")
    print(f"Output tokens: {result['output_tokens']}")
    print(f"Input cost: {result['input_cost']}")
    print(f"Output cost: {result['output_cost']}")
    print(f"Total cost: {result['total_cost']}")
