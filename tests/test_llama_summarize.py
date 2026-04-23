"""Test llama summarizer function."""

import json
from unittest.mock import MagicMock, patch

import pytest
import requests  # type: ignore[import-untyped]

from restaurant_review.summarizer import llama_summarize


def test_llama_summarize_returns_response():
    """Test llama_summarize: Correct response."""
    mock_response = MagicMock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {
        "response": '{"restaurantName": "Pizza Place",'
        '"foodQuality": 8,'
        ' "service": 7,'
        ' "value": 6,'
        ' "overallSentiment": "positive",'
        ' "summary": "great place",'
        ' "reason": "good food"}'
    }

    with patch(
        "restaurant_review.summarizer.requests.post", return_value=mock_response
    ):
        result = llama_summarize(["good food", "great service"], "Pizza Place")

    assert result == {
        "restaurantName": "Pizza Place",
        "foodQuality": 8,
        "service": 7,
        "value": 6,
        "overallSentiment": "positive",
        "summary": "great place",
        "reason": "good food",
    }


def test_llama_summarize_connection_failure():
    """Test llama_summarize: Failed to connect to llama."""
    with (
        patch(
            "restaurant_review.summarizer.requests.post",
            side_effect=requests.exceptions.RequestException,
        ),
        pytest.raises(requests.exceptions.RequestException),
    ):
        llama_summarize(["good food", "great service"], "Pizza Place")


def test_llama_summarize_json_error():
    """Test llama_summarize: failure to convert to JSON."""
    mock_response = MagicMock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {"response": "{not valid json}"}

    with (
        patch(
            "restaurant_review.summarizer.requests.post",
            return_value=mock_response,
        ),
        pytest.raises(json.JSONDecodeError),
    ):
        llama_summarize(["good food", "great service"], "Pizza Place")


def test_llama_summarize_missing_response():
    """Test llama_summarize: Missing response key."""
    mock_response = MagicMock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {"response": "no json here at all"}

    with (
        patch(
            "restaurant_review.summarizer.requests.post",
            return_value=mock_response,
        ),
        pytest.raises(ValueError),
    ):
        llama_summarize(["good food", "great service"], "Pizza Place")
