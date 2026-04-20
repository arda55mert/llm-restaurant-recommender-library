"""ranking the restaurants based on summaries."""


def compute_score(data, weights):
    """It is computing a weighted score for a restaurant."""
    return (
        weights["food"] * data["foodQuality"]
        + weights["service"] * data["service"]
        + weights["value"] * data["value"]
    )
