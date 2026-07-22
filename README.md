# Multi-Provider News Summarizer

This project builds a simple workflow that takes news articles as input, fetches them from the News API, summarizes them with OpenAI, analyzes sentiment with Cohere, and returns a structured output payload that can be reviewed end to end.

## What the project does

- Pulls recent technology news from the News API
- Sends article content to OpenAI for summarization
- Sends article content to Cohere for sentiment-style analysis
- Produces a reviewable output record with article count, summaries, and cost information

## Setup

1. Create and activate a Python environment.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Copy the environment template and add your real API keys:
   ```bash
   cp .env.example .env
   ```
4. Fill in the values for:
   - `OPENAI_API_KEY`
   - `COHERE_API_KEY`
   - `NEWS_API_KEY`

## How to run it

Run the application:

```bash
python main.py
```

Run the tests:

```bash
pytest -q
```

## Example output

The workflow prints a payload containing:
- `article_count`
- `summaries`
- `cost_summary`

## Cost analysis

The workflow tracks a simple cost summary for each provider call. In the current run, the cost summary reported a total of approximately `$0.0054` across the executed provider steps.

## Notes on reliability

The workflow includes safeguards for missing configuration and for provider-call failures so it can still return a controlled output instead of crashing.

