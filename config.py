import os
from typing import Dict, List

from dotenv import load_dotenv

load_dotenv()


def load_config() -> Dict[str, str]:
    """Load configuration from environment variables."""
    return {
        "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY", ""),
        "COHERE_API_KEY": os.getenv("COHERE_API_KEY", ""),
        "NEWS_API_KEY": os.getenv("NEWS_API_KEY", ""),
        "ENVIRONMENT": os.getenv("ENVIRONMENT", "development"),
        "MAX_RETRIES": os.getenv("MAX_RETRIES", "3"),
        "REQUEST_TIMEOUT": os.getenv("REQUEST_TIMEOUT", "30"),
        "DAILY_BUDGET": os.getenv("DAILY_BUDGET", "5.00"),
    }


def validate_config(config: Dict[str, str]) -> List[str]:
    """Return a list of missing required configuration keys."""
    required_keys = ["OPENAI_API_KEY", "COHERE_API_KEY", "NEWS_API_KEY"]
    return [key for key in required_keys if not config.get(key)]


if __name__ == "__main__":
    config = load_config()
    missing = validate_config(config)
    if missing:
        print("Missing required configuration:", ", ".join(missing))
    else:
        print("Configuration is valid.")
