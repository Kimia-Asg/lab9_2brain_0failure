import os
from typing import List, Dict

import requests

from config import load_config


class NewsAPIClient:
    """Fetch news articles from the News API service."""

    def __init__(self, api_key: str | None = None) -> None:
        self.api_key = api_key or load_config().get("NEWS_API_KEY", "")
        self.base_url = "https://newsapi.org/v2/top-headlines"

    def fetch_top_headlines(self, category: str = "technology", country: str = "us", limit: int = 3) -> List[Dict[str, str]]:
        """Return a limited list of article dictionaries."""
        if not self.api_key:
            return [
                {
                    "title": "Demo article",
                    "description": "No API key configured; using demo article.",
                    "url": "https://example.com/demo",
                }
            ]

        params = {
            "country": country,
            "category": category,
            "apiKey": self.api_key,
        }
        response = requests.get(self.base_url, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
        articles = data.get("articles", [])[:limit]
        return [
            {
                "title": article.get("title", "Untitled"),
                "description": article.get("description", ""),
                "url": article.get("url", ""),
            }
            for article in articles
        ]


if __name__ == "__main__":
    client = NewsAPIClient()
    articles = client.fetch_top_headlines(limit=3)
    for article in articles:
        print(f"- {article['title']}")
