# Multi-Provider News Summarizer

This project builds a simple workflow that takes news articles as input, summarizes them with an OpenAI-style provider, analyzes sentiment with a Cohere-style provider, and returns a structured output payload.

## Setup

1. Create a virtual environment and install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Copy the example environment file and add your API keys:
   ```bash
   cp .env.example .env
   ```

## Run the workflow

```bash
python main.py
```

## Example output

The program prints a payload with:
- `article_count`
- `summaries`
- `cost_summary`

## Cost notes

The current implementation uses lightweight simulated provider calls so it is safe to run without real API credentials. In a production version, these calls would be replaced with real API requests and actual cost tracking.
