"""user interface."""

from fasthtml.common import (  # type: ignore[import-untyped]
    H1,
    H3,
    Button,
    Div,
    FastHTML,
    Form,
    Input,
    Label,
    Option,
    P,
    Select,
)

from restaurant_review.loader import load_reviews
from restaurant_review.pipeline import getTopRestaurants

# initializing FastHTML
app = FastHTML()


@app.get("/")
def home():
    """FastHTML of the first page."""
    return Div(
        Div(
            H1("Restaurant Finder", style="margin-bottom:20px;"),
            # form for user input
            Form(
                # city selection
                Div(
                    Label("City"),
                    Select(
                        Option("Durham"),
                        Option("Nashville"),
                        Option("Dallas"),
                        Option("San Diego"),
                        Option("New York"),
                        name="city",
                    ),
                    style="margin-bottom:15px;",
                ),
                # cuisine selection
                Div(
                    Label("Cuisine"),
                    Select(
                        Option("Japanese"),
                        Option("American"),
                        Option("Turkish"),
                        Option("Italian"),
                        Option("Mediterranean"),
                        Option("Mexican"),
                        Option("French"),
                        Option("Indian"),
                        Option("Thai"),
                        Option("Korean"),
                        name="cuisine",
                    ),
                    style="margin-bottom:15px;",
                ),
                # sorting preference
                Div(
                    Label("Sort By"),
                    Select(
                        Option("Overall"),
                        Option("Food"),
                        Option("Service"),
                        Option("Value"),
                        name="sort_by",
                    ),
                    style="margin-bottom:15px;",
                ),
                # slider for food importance weight
                Div(
                    Label("Food Importance"),
                    Input(
                        type="range", min="0", max="1", step="0.1", name="food"
                    ),
                    style="margin-bottom:15px;",
                ),
                # slider for service importance weight
                Div(
                    Label("Service Importance"),
                    Input(
                        type="range",
                        min="0",
                        max="1",
                        step="0.1",
                        name="service",
                    ),
                    style="margin-bottom:15px;",
                ),
                # slider for value importance weight
                Div(
                    Label("Value Importance"),
                    Input(
                        type="range", min="0", max="1", step="0.1", name="value"
                    ),
                    style="margin-bottom:20px;",
                ),
                # submit button
                Button("Search", style="padding:10px 20px;"),
                method="post",  # sending via POST
                action="/search",
            ),
            # layout of form
            style="""
                background:white;
                padding:40px;
                border-radius:10px;
                box-shadow:0 4px 12px rgba(0,0,0,0.1);
                width:350px;
                text-align:center;
            """,
        ),
        # full-page layout
        style="""
            height:100vh;
            display:flex;
            justify-content:center;
            align-items:center;
            background:#f5f7fa;
            font-family:Arial;
        """,
    )


@app.post("/search")
def search(
    city: str,
    cuisine: str,
    food: float,
    service: float,
    value: float,
    sort_by: str,
):
    """FastHTML of the second page."""
    # loading the dataset
    df = load_reviews("data/SyntheticRestaurantReviews.csv")

    # constructing the weights dictionary
    weights = {
        "food": float(food),
        "service": float(service),
        "value": float(value),
    }

    # running the pipeline
    results = getTopRestaurants(df, city, cuisine, weights, sort_by)

    # forming the content
    content = (
        [P("No restaurants were found for your selection.")]
        if not results
        else [
            Div(
                Div(
                    H3(
                        f"{i + 1}. {r['restaurantName']} ⭐ {r['rating']} "
                        f"({r['price']})"
                    ),
                    P(f"Score: {round(r['score'], 2)}"),
                    style="display:flex; justify-content:space-between; "
                    "align-items:center;",
                ),
                # number of reviews
                P(f"{r['reviews']} reviews", style="color:#666;"),
                # metrics of the restaurant
                Div(
                    P(f"Food: {r['foodQuality']}/10"),
                    P(f"Service: {r['service']}/10"),
                    P(f"Value: {r['value']}/10"),
                    style="display:flex; gap:20px;",
                ),
                # explanations from LLaMA
                P(
                    f"reasoning: {r['reason']}",
                    style="font-style:italic; color:#787878;",
                ),
                # summary of reviews
                P(r["summary"]),
                # highlighting top-ranked restaurant
                P("Best Pick", style="color:green;") if i == 0 else None,
                style="""
                    margin-bottom:25px;
                    padding-bottom:10px;
                    border-bottom:1px solid #ccc;
                """,
            )
            for i, r in enumerate(results)
        ]
    )
    # returning results page
    return Div(
        Div(
            H1(f"{cuisine} Restaurant Recommendations in {city}"),
            # back button to return to home page
            Button(
                "← Back",
                onclick="window.location.href='/'",
                style="margin-bottom;",
            ),
            # inserting generated content into the page
            # * unpacking the list into individual components
            *content,
            style="""
                background:white;
                padding:40px;
                border-radius:10px;
                box-shadow:0 4px 12px rgba(0,0,0,0.1);
                width:700px;
            """,
        ),
        style="""
            min-height:100vh;
            display:flex;
            justify-content:center;
            align-items:flex-start;
            padding-top:50px;
            background:#f5f7fa;
            font-family:Arial;
        """,
    )
