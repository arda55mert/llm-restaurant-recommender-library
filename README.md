# Restaurant Finder

an interactive web application that analyzes restaurant reviews using a Large Language Model (LLaMA) to generate summaries and rank restaurants based on user preferences.

---

## Features

- filtering restaurants by **city** and **cuisine**
- aggregating and summarizing reviews using **LLaMA**
- ranking restaurants based on:
  - food quality
  - service
  - value
- adjustable importance weights
- multiple sorting options (Overall, Food, Service, Value)
- reasoning for top restaurant recommendations

---

## How?

1. **Filter**
   - select city + cuisine
   - dataset is filtered accordingly

2. **Summarize**
   - up to fifty reviews per restaurant are sent to LLaMA
   - model returns:
     - food / service / value scores
     - summary
     - reasoning

3. **Score**
   - custom scoring function combines:
     ```
     score = w_food * foodQuality +
             w_service * service +
             w_value * value
     ```

4. **Rank**
   - restaurants are sorted based on user-selected criteria
---

## Installation

Please, clone the repository by using the following codes from terminal:

```bash
git clone git@github.com:arda55mert/llm-restaurant-recommender-library.git
cd restaurant-review-library
pip install .
```

## start the app

```bash
docker compose up --build
```

## testing
```bash
pytest
```

## AI Disclosure
We used ChatGPT to generate a synthetic dataset of restaurant reviews by prompting it to create approximately 100,000 entries in CSV format, including restaurant names, cities (Durham, Nashville, San Diego, Dallas, New York), cuisine types, price ranges, customer ratings and varied-length customer comments with both positive and negative feedback. GPT produced a diverse, non-repetitive set of reviews with a range of star ratings and detail levels, which we used as input data to develop and test the restaurant recommendation and summarization pipeline. 

Additionally ChatGPT provided small-scale assistance with generating Dockerfile templates, debugging issues, recommending the unittest.mock package for testing, and offering styling suggestions for the frontend page layout.

