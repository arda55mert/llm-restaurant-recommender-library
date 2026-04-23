"""summarizing the reviews."""

import json
import os

import requests  # type: ignore[import-untyped]


def llama_summarize(reviews, restaurant_name):
    """It is summarizing list of restaurant reviews using LLaMA."""
    text = "\n".join(reviews)

    prompt = f"""

    Return exactly one JSON object and nothing else.

    Keys:
    - restaurantName: string
    - foodQuality: integer 1 to 10
    - service: integer 1 to 10
    - value: integer 1 to 10
    - overallSentiment: positive, neutral, or negative
    - summary: 2 to 3 sentence summary
    - reason: 1 short sentence

    Return this JSON structure:
    {{
    "restaurantName": "<restaurant name>",
    "foodQuality": <1-10>,
    "service": <1-10>,
    "value": <1-10>,
    "overallSentiment": "<positive|neutral|negative>",
    "summary": "<2-3 sentence summary>",
    "reason": "<1 short sentence>"
    }}

    Restaurant: {restaurant_name}
    Reviews:
    {text}
    """

    response = requests.post(
        os.getenv("OLLAMA_URL", "http://ollama:11434/api/generate"),
        json={
            "model": os.getenv("OLLAMA_MODEL", "llama3"),
            "prompt": prompt,
            "stream": False,
        },
        timeout=180,
    )
    response.raise_for_status()

    json_response = response.json()
    response_text = json_response["response"].strip()

    print("RAW MODEL RESPONSE:", response_text)

    start = response_text.find("{")
    end = response_text.rfind("}")

    if start == -1 or end == -1 or end <= start:
        raise ValueError("Model did not return JSON.")

    candidate = response_text[start : end + 1]
    return json.loads(candidate)
