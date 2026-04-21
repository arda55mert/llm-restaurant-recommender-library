"""summarizing the reviews."""

import os

import requests  # type: ignore[import-untyped]


def llama_summarize(reviews, restaurant_name):
    """It is summarizing list of restaurant reviews using LLaMA."""
    text = "\n".join(reviews)

    prompt = f"""
    you are analyzing all reviews for one restaurant.

    aggregate all reviews into one summary.

    do not summarize each review separately.
    do not return multiple objects.
    return only one JSON object.

    Format:
    {{
    "restaurantName": "{restaurant_name}",
    "foodQuality": 1-10,
    "service": 1-10,
    "value": 1-10,
    "overallSentiment": "positive/neutral/negative",
    "summary": "two-three sentence thorough summary",
    "reason": "one short sentence explaining why this restaurant ranks well"
    }}

    Reviews:
    {text}
    """
    try:
        response = requests.post(
            os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate"),
            json={
                "model": os.getenv("OLLAMA_MODEL", "llama3"),
                "prompt": prompt,
                "stream": False,
            },
            timeout=180,
        )
        json_response = response.json()
        return json_response["response"]

    except Exception:
        return ""
