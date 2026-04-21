"""summarizing the reviews."""

import json
import os
import re

import requests  # type: ignore[import-untyped]


def llama_summarize(reviews, restaurant_name):
    """Summarize restaurant reviews using LLaMA and return one parsed JSON object."""
    text = "\n".join(reviews)

    prompt = f"""
You are analyzing all reviews for one restaurant.

Aggregate all reviews into one summary.
Do not summarize each review separately.
Do not return multiple objects.
Return only one valid JSON object.
Do not include markdown fences.
Do not include any text before or after the JSON.

Format:
{{
  "restaurantName": "{restaurant_name}",
  "foodQuality": 1,
  "service": 1,
  "value": 1,
  "overallSentiment": "positive",
  "summary": "two-three sentence thorough summary",
  "reason": "one short sentence explaining why this restaurant ranks well"
}}

Reviews:
{text}
"""

    fallback = {
        "restaurantName": restaurant_name,
        "foodQuality": 5,
        "service": 5,
        "value": 5,
        "overallSentiment": "neutral",
        "summary": "Summary unavailable.",
        "reason": "Model output could not be parsed.",
    }

    try:
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
        response_text = json_response.get("response", "").strip()

        print("RAW MODEL RESPONSE:", response_text)

        match = re.search(r"\{.*\}", response_text, re.DOTALL)
        if not match:
            return fallback

        parsed = json.loads(match.group(0))

        parsed.setdefault("restaurantName", restaurant_name)
        parsed.setdefault("foodQuality", 5)
        parsed.setdefault("service", 5)
        parsed.setdefault("value", 5)
        parsed.setdefault("overallSentiment", "neutral")
        parsed.setdefault("summary", "Summary unavailable.")
        parsed.setdefault("reason", "Model output could not be parsed.")

        return parsed

    except Exception as e:
        print("SUMMARIZER ERROR:", e)
        return fallback