"""loading the reviews."""

import pandas as pd  # type: ignore[import-untyped]


def load_reviews(path):
    """It is loading restaurant reviews and group them by restaurant name."""
    return pd.read_csv(path)
