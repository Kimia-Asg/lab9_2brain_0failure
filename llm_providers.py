import os
from typing import Dict, List

import cohere
from dotenv import load_dotenv

from config import load_config

load_dotenv(dotenv_path='.env')


class LLMProvider:
    """Real provider wrapper for OpenAI and Cohere with cost tracking."""

    def __init__(self, provider_name: str) -> None:
        self.provider_name = provider_name
        config = load_config()
        self.openai_key = config.get("OPENAI_API_KEY", "")
        self.cohere_key = config.get("COHERE_API_KEY", "")

    def generate_text(self, prompt: str) -> Dict[str, object]:
        """Call a real provider API and return the response plus estimated cost."""
        safe_prompt = (prompt or "Please provide a short response.").strip()
        if not safe_prompt:
            safe_prompt = "Please provide a short response."

        if self.provider_name == "openai":
            if not self.openai_key:
                return {
                    "provider": self.provider_name,
                    "text": "Fallback response: OpenAI API key is missing.",
                    "cost_usd": 0.0,
                }
            try:
                from openai import OpenAI

                client = OpenAI(api_key=self.openai_key)
                response = client.responses.create(
                    model="gpt-4o-mini",
                    input=safe_prompt,
                )
                text = response.output_text
                cost_usd = 0.001
                return {
                    "provider": self.provider_name,
                    "text": text,
                    "cost_usd": cost_usd,
                }
            except Exception:
                return {
                    "provider": self.provider_name,
                    "text": "Fallback response: OpenAI call failed.",
                    "cost_usd": 0.0,
                }

        if self.provider_name == "cohere":
            if not self.cohere_key:
                return {
                    "provider": self.provider_name,
                    "text": "Fallback response: Cohere API key is missing.",
                    "cost_usd": 0.0,
                }
            try:
                client = cohere.Client(self.cohere_key)
                response = client.chat(
                    model="command-r-08-2024",
                    message=safe_prompt,
                )
                text = getattr(response, "text", str(response))
                cost_usd = 0.0008
                return {
                    "provider": self.provider_name,
                    "text": text,
                    "cost_usd": cost_usd,
                }
            except Exception:
                return {
                    "provider": self.provider_name,
                    "text": "Fallback response: Cohere call failed.",
                    "cost_usd": 0.0,
                }

        return {
            "provider": self.provider_name,
            "text": "Fallback response: unsupported provider.",
            "cost_usd": 0.0,
        }


class CostTracker:
    """Track cumulative API costs for the workflow."""

    def __init__(self) -> None:
        self.costs: List[Dict[str, object]] = []

    def add_cost(self, provider: str, amount: float) -> None:
        self.costs.append({"provider": provider, "amount_usd": amount})

    def total(self) -> float:
        return sum(float(item["amount_usd"]) for item in self.costs)


if __name__ == "__main__":
    config = load_config()
    print("Configuration loaded:", bool(config.get("OPENAI_API_KEY")) and bool(config.get("COHERE_API_KEY")))
    openai_provider = LLMProvider("openai")
    cohere_provider = LLMProvider("cohere")
    print(openai_provider.generate_text("Summarize this article"))
    print(cohere_provider.generate_text("Analyze sentiments"))
