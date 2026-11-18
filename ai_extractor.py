import json
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

from database import get_all_products

env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)
client = Groq()


def extract_order_from_txt(message: str) -> dict:
    products = get_all_products()
    catalog_names = [p["name"] for p in products]

    system_prompt = f"""You are an automated customer service assistant.
Our store sells these exact products: {catalog_names}

Analyze the customer message to extract what they want to order. Match their item to the closest exact product name from our catalog list above when possible.
You must respond ONLY with a raw JSON object with these exact keys:
- "intent": string — must be ONLY one of:
    "ORDER" (customer clearly wants to buy AND named a specific product)
    "INCOMPLETE" (customer wants to buy, but did not name a specific product)
    "INQUIRY" (customer is just greeting or asking a question)
- "is_order": boolean (true ONLY if intent is "ORDER", otherwise false)
- "customer": string (the customer's name, or "Customer" if not mentioned)
- "product": string (the exact product name from our catalog if it matches, otherwise the item they asked for, or "" if not an order)
- "quantity": integer (number of items as an integer, default to 1 if not specified)

Do not add any explanation or markdown formatting. Output pure JSON only."""

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": str(message)},
        ],
        response_format={"type": "json_object"},
        temperature=0.0,
    )

    data = json.loads(response.choices[0].message.content)
    data["is_order"] = bool(data.get("is_order", False))
    data["customer"] = (data.get("customer") or "Customer").strip()
    data["product"] = (data.get("product") or "").strip()

    try:
        data["quantity"] = int(data.get("quantity") or 1)
    except (ValueError, TypeError):
        data["quantity"] = 1

    return data


if __name__ == "__main__":
    sample_message = "I want to order 2 Black Hoodies, my name is Suman."
    print("Customer Message:", sample_message)
    order_data = extract_order_from_txt(sample_message)
    print("\nExtracted Data from AI:")
    print(order_data)
    print("Data Type:", type(order_data))
    