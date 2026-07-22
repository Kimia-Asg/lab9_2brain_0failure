from typing import Dict, List

from llm_providers import CostTracker, LLMProvider
from news_api import NewsAPIClient


class NewsSummarizer:
    """Build a simple multi-provider workflow for summarizing news articles."""

    def __init__(self) -> None:
        self.news_client = NewsAPIClient()
        self.cost_tracker = CostTracker()

    def summarize_article(self, article: Dict[str, str]) -> Dict[str, object]:
        """Create a summary and sentiment result for one article."""
        openai_provider = LLMProvider("openai")
        cohere_provider = LLMProvider("cohere")

        summary_result = openai_provider.generate_text(article.get("title", ""))
        sentiment_result = cohere_provider.generate_text(article.get("description", ""))

        self.cost_tracker.add_cost("openai", summary_result["cost_usd"])
        self.cost_tracker.add_cost("cohere", sentiment_result["cost_usd"])

        return {
            "title": article.get("title", "Untitled"),
            "summary": summary_result["text"],
            "sentiment": sentiment_result["text"],
            "url": article.get("url", ""),
        }

    def run_workflow(self, articles: List[Dict[str, str]] | None = None, article_limit: int = 2) -> Dict[str, object]:
        """Run the full input -> transform -> output workflow."""
        if articles is None:
            articles = self.news_client.fetch_top_headlines(limit=article_limit)

        summaries = [self.summarize_article(article) for article in articles[:article_limit]]
        return {
            "article_count": len(summaries),
            "summaries": summaries,
            "cost_summary": {
                "total_cost_usd": round(self.cost_tracker.total(), 4),
                "provider_breakdown": self.cost_tracker.costs,
            },
        }


if __name__ == "__main__":
    summarizer = NewsSummarizer()
    result = summarizer.run_workflow(article_limit=2)
    print(result)
