"""processing & ranking the reviews."""

import json
import random
import re

from restaurant_review.ranker import compute_score
from restaurant_review.summarizer import llama_summarize


def getTopRestaurants(df, city, cuisine, weights, sort_by="Overall", topK=3):
    """It is filtering, summarizing and ranking restaurants."""
    
    # filtering dataset by selected city and cuisine - case insensitive and ignoring leading/trailing spaces
    filtered = df[
        (df["City"].str.strip().str.lower() == city.strip().lower()) &
        (df["Cuisine"].str.strip().str.lower().str.contains(cuisine.strip().lower()))
    ]

    # if no restaurants match, return empty list
    if filtered.empty:
        return []

    # grouping by restaurant
    grouped = filtered.groupby("Restaurant Name").agg(
        {
            "Customer Review": list,
            "Customer Star": "mean",
            "Price Range": "first",
        }
    )

    # limiting to top 5 restaurants by average rating to reduce LLaMA calls
    grouped = grouped.sort_values("Customer Star", ascending=False).head(5)
    results = []

    # iterating through each restaurant
    for restaurant, row in grouped.iterrows():
        reviews = row["Customer Review"]
        AVGrating = row["Customer Star"]
        priceRange = row["Price Range"]

        # skipping if no reviews
        if not reviews:
            continue

        # sampling eight reviews to send to LLaMA
        sample = random.sample(reviews, min(8, len(reviews)))

        # calling LLaMA to summarize reviews
        parsed = llama_summarize(sample, restaurant)

        # computing overall score based on user weights
        try:
            score = compute_score(parsed, weights)
        except Exception:
            continue

        results.append(
            {
                "restaurantName": restaurant,
                "score": score,
                "summary": parsed.get("summary", ""),
                "foodQuality": parsed.get("foodQuality", 0),
                "service": parsed.get("service", 0),
                "value": parsed.get("value", 0),
                "rating": round(AVGrating, 1),
                "price": priceRange,
                "reason": parsed.get("reason", ""),
                "reviews": len(reviews),
            }
        )
    # sorting options
    keyMap = {
        "Overall": lambda x: x["score"],
        "Food": lambda x: x["foodQuality"],
        "Service": lambda x: x["service"],
        "Value": lambda x: x["value"],
    }
    # sorting key
    sortKey = keyMap.get(sort_by, keyMap["Overall"])
    # sorting results in descending order
    results = sorted(results, key=sortKey, reverse=True)

    # returning top K restaurants
    return results[:topK]
