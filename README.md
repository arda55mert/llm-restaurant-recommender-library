# Restaurant Finder

An interactive web application that analyzes restaurant reviews using a Large Language Model (LLaMA) to generate summaries and rank restaurants based on user preferences.

---

## Features

- Filter restaurants by **city** and **cuisine**
- Aggregate and summarize reviews using **LLaMA**
- Rank restaurants based on food quality, service, and value
- Adjustable importance weights
- Multiple sorting options (Overall, Food, Service, Value)
- Reasoning for top restaurant recommendations

---

## How it works

1. **Filter** — select city and cuisine; the dataset is filtered accordingly
2. **Summarize** — up to 50 reviews per restaurant are sent to LLaMA, which returns food / service / value scores, a summary, and reasoning
3. **Score** — a custom scoring function combines the scores:
   ```
   score = w_food * foodQuality + w_service * service + w_value * value
   ```
4. **Rank** — restaurants are sorted based on user-selected criteria

---

## Installation

```bash
git clone git@github.com:arda55mert/llm-restaurant-recommender-library.git
cd llm-restaurant-recommender-library
pip install .
```

---

## Running the app

> **Prerequisites:** [Docker](https://docs.docker.com/get-docker/) and ~4 GB of free disk space for the LLaMA 3 model.

```bash
docker compose up --build
```

Then open http://localhost:8000 in your browser.

On first run, Docker will pull the LLaMA 3 model (~4 GB). Subsequent runs will be faster.

To stop:

```bash
docker compose down
```

**Environment variables** — set automatically by `docker-compose.yml`, no manual configuration needed:

| Variable | Value |
|---|---|
| `OLLAMA_URL` | `http://ollama:11434/api/generate` |
| `OLLAMA_MODEL` | `llama3` |

---

## Testing

```bash
pytest
```

---

## AI Disclosure

We used ChatGPT to generate a synthetic dataset of restaurant reviews by prompting it to create approximately 100,000 entries in CSV format, including restaurant names, cities (Durham, Nashville, San Diego, Dallas, New York), cuisine types, price ranges, customer ratings, and varied-length customer comments with both positive and negative feedback. GPT produced a diverse, non-repetitive set of reviews with a range of star ratings and detail levels, which we used as input data to develop and test the restaurant recommendation and summarization pipeline.

Additionally, ChatGPT provided small-scale assistance with generating Dockerfile templates, debugging issues, recommending the `unittest.mock` package for testing, and offering styling suggestions for the frontend page layout.
