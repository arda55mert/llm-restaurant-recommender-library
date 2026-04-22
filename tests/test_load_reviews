"""Tests for the loader function."""

import pandas as pd
import pytest

from restaurant_review.loader import load_reviews


def test_load_review_returns_df(tmp_path):
    """Test load_review: Structure of return object."""
    path = tmp_path / "reviews.csv"
    path.write_text("restaurant,review\nPizza Place,Great!\nBurger Place,Ok")
    result = load_reviews(path)
    assert isinstance(result, pd.DataFrame)
    assert len(result) == 2


def test_load_reviews_file_not_found():
    """Test load_reviews: Incorrect file path."""
    with pytest.raises(FileNotFoundError):
        load_reviews("nonexistent.csv")
