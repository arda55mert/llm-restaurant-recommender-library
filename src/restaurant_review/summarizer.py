"""summarizing the reviews."""

import json
import re

import requests  # type: ignore[import-untyped]


def llama_summarize(reviews, restaurant_name):
    """It is summarizing list of restaurant reviews using LLaMA."""
    text = "\n".join(reviews)

    prompt = f"""
    you are analyzing all reviews for one restaurant.

    aggregate all reviews into one summary.

    do not summarize each review separately.
    do not return multiple objects.
    return only one valid JSON object.
    do not include markdown fences.
    do not include any text before or after the JSON.

    Format:
    {{
    "restaurantName": "{restaurant_name}",
    "foodQuality": 1-10,
    "service": 1-10,
    "value": 1-10,
    "overallSentiment": "positive",
    "summary": "two-three sentence thorough summary",
    "reason": "one short sentence explaining why this restaurant ranks well"
    }}

    Reviews:
    {text}
    """

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3",
            "prompt": prompt,
            "stream": False,
        },
        timeout=180,
    )
    response.raise_for_status()

    json_response = response.json()
    response_text = json_response["response"].strip()

    match = re.search(r"\{.*\}", response_text, re.DOTALL)
    if not match:
        raise ValueError("Model did not return JSON.")

    return json.loads(match.group(0))