"""Test compute_score function."""

import pytest

from restaurant_review.ranker import compute_score


def test_compute_score_calculation():
    """Test compute_score function: Calculation."""
    data = {"foodQuality": 8, "service": 6, "value": 7}
    weights = {"food": 0.5, "service": 0.3, "value": 0.2}
    result = compute_score(data, weights)
    assert result == 0.5 * 8 + 0.3 * 6 + 0.2 * 7


def test_compute_score_zero_weight():
    """Test compute_score function: 0 weights produce 0 score."""
    data = {"foodQuality": 8, "service": 6, "value": 7}
    weights = {"food": 0, "service": 0, "value": 0}
    result = compute_score(data, weights)
    assert result == 0


def test_compute_score_missing_data():
    """Test compute_score function: Column missing."""
    data = {"foodQuality": 8, "service": 6}
    weights = {"food": 0.5, "service": 0.3, "value": 0.2}
    with pytest.raises(KeyError):
        compute_score(data, weights)
