"""Tests for getTopRestaurants function."""

import pandas as pd
from unittest.mock import patch

from restaurant_review.pipeline import getTopRestaurants


def test_get_top_restaurants_no_match():
    """Test getTopRestaurants: No matching restaurant."""
    df = pd.DataFrame(
        {
            "City": ["New York"],
            "Cuisine": ["Italian"],
            "Restaurant Name": ["Pizza Place"],
            "Customer Review": ["great food"],
            "Customer Star": [4.5],
            "Price Range": ["$$"],
        }
    )

    result = getTopRestaurants(
        df, "Boston", "Italian", {"food": 1, "service": 1, "value": 1}
    )

    assert result == []


def test_get_top_restaurants_correct_structure():
    """Test getTopRestaurants: Correct Result Structure."""
    df = pd.DataFrame(
        {
            "City": ["New York"],
            "Cuisine": ["Italian"],
            "Restaurant Name": ["Pizza Place"],
            "Customer Review": ["great food"],
            "Customer Star": [4.5],
            "Price Range": ["$$"],
        }
    )

    mock_summary = {
        "foodQuality": 8,
        "service": 7,
        "value": 6,
        "overallSentiment": "positive",
        "summary": "great place",
        "reason": "good food",
    }

    with patch(
        "restaurant_review.pipeline.llama_summarize", return_value=mock_summary
    ):
        result = getTopRestaurants(
            df, "New York", "Italian", {"food": 1, "service": 1, "value": 1}
        )

    assert len(result) == 1
    assert result[0]["restaurantName"] == "Pizza Place"
    assert result[0]["foodQuality"] == 8
    assert result[0]["service"] == 7
    assert result[0]["value"] == 6
    assert result[0]["rating"] == 4.5
    assert result[0]["price"] == "$$"


def test_get_top_restaurants_returns_top_k():
    """Test getTopRestaurants: Returns correct number of results."""
    df = pd.DataFrame(
        {
            "City": ["New York", "New York", "New York"],
            "Cuisine": ["Italian", "Italian", "Italian"],
            "Restaurant Name": ["Pizza Place", "Pasta Place", "Olive Garden"],
            "Customer Review": ["great food", "nice place", "decent food"],
            "Customer Star": [4.5, 4.0, 3.5],
            "Price Range": ["$$", "$$", "$"],
        }
    )

    mock_summary = {
        "foodQuality": 8,
        "service": 7,
        "value": 6,
        "overallSentiment": "positive",
        "summary": "great place",
        "reason": "good food",
    }
    with patch(
        "restaurant_review.pipeline.llama_summarize", return_value=mock_summary
    ):
        result = getTopRestaurants(
            df,
            "New York",
            "Italian",
            {"food": 1, "service": 1, "value": 1},
            topK=2,
        )

    assert len(result) == 2


def test_get_top_restaurants_sorted_by_food():
    """Test getToprestaurants: Correct sorting."""
    df = pd.DataFrame(
        {
            "City": ["New York", "New York"],
            "Cuisine": ["Italian", "Italian"],
            "Restaurant Name": ["Pizza Place", "Pasta Place"],
            "Customer Review": ["great food", "nice place"],
            "Customer Star": [4.5, 4.0],
            "Price Range": ["$$", "$$"],
        }
    )

    mock_summary_high = {
        "foodQuality": 9,
        "service": 7,
        "value": 6,
        "overallSentiment": "positive",
        "summary": "great place",
        "reason": "good food",
    }
    mock_summary_low = {
        "foodQuality": 5,
        "service": 7,
        "value": 6,
        "overallSentiment": "positive",
        "summary": "decent place",
        "reason": "ok food",
    }

    with patch(
        "restaurant_review.pipeline.llama_summarize",
        side_effect=[mock_summary_high, mock_summary_low],
    ):
        result = getTopRestaurants(
            df,
            "New York",
            "Italian",
            {"food": 1, "service": 0, "value": 0},
            sort_by="Food",
        )

    assert result[0]["restaurantName"] == "Pizza Place"
    assert result[1]["restaurantName"] == "Pasta Place"


def test_get_top_restaurants_skips_failed_summarize():
    """Test getTopRestaurants: Function skips unsummarized restaurants."""
    df = pd.DataFrame(
        {
            "City": ["New York", "New York"],
            "Cuisine": ["Italian", "Italian"],
            "Restaurant Name": ["Pizza Place", "Pasta Place"],
            "Customer Review": ["great food", "nice place"],
            "Customer Star": [4.5, 4.0],
            "Price Range": ["$$", "$$"],
        }
    )

    mock_summary = {
        "foodQuality": 8,
        "service": 7,
        "value": 6,
        "overallSentiment": "positive",
        "summary": "great place",
        "reason": "good food",
    }

    with patch(
        "restaurant_review.pipeline.llama_summarize",
        side_effect=[{}, mock_summary],
    ):
        result = getTopRestaurants(
            df, "New York", "Italian", {"food": 1, "service": 1, "value": 1}
        )

    assert len(result) == 1
    assert result[0]["restaurantName"] == "Pasta Place"
