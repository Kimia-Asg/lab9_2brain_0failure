import os

from config import load_config, validate_config
from llm_providers import LLMProvider
from summarizer import NewsSummarizer


def test_run_workflow_returns_summary_payload():
    summarizer = NewsSummarizer()
    articles = [
        {
            "title": "AI agents automate support tasks",
            "description": "Teams are using AI agents to speed up internal support workflows.",
            "url": "https://example.com/agent-support",
        }
    ]

    result = summarizer.run_workflow(articles=articles, article_limit=1)

    assert result["article_count"] == 1
    assert result["summaries"][0]["title"] == "AI agents automate support tasks"
    assert "summary" in result["summaries"][0]
    assert result["cost_summary"]["total_cost_usd"] >= 0


def test_validate_config_reports_missing_keys(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("COHERE_API_KEY", raising=False)
    monkeypatch.setenv("NEWS_API_KEY", "demo-key")
    monkeypatch.setenv("ENVIRONMENT", "development")

    config = load_config()
    missing = validate_config(config)

    assert "OPENAI_API_KEY" in missing
    assert "COHERE_API_KEY" in missing
    assert "NEWS_API_KEY" not in missing


def test_provider_handles_empty_prompt():
    provider = LLMProvider("cohere")
    result = provider.generate_text("")

    assert result["provider"] == "cohere"
    assert isinstance(result["text"], str)
    assert len(result["text"]) > 0


def test_provider_falls_back_when_api_call_fails(monkeypatch):
    def fail_client(*args, **kwargs):
        raise RuntimeError("provider unavailable")

    monkeypatch.setattr("llm_providers.cohere.Client", fail_client)
    provider = LLMProvider("cohere")
    result = provider.generate_text("Summarize this")

    assert result["provider"] == "cohere"
    assert "Fallback" in result["text"]
    assert result["cost_usd"] == 0.0
