import os
from pydantic import BaseModel
from typing import List

class Settings(BaseModel):
    # Application settings
    APP_NAME: str = "News API"
    DEBUG: bool = os.getenv("DEBUG", "False") == "True"
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    
    # Elasticsearch settings
    ELASTICSEARCH_URL: str = os.getenv("ELASTICSEARCH_URL", "http://localhost:9200")
    ELASTICSEARCH_USERNAME: str = os.getenv("ELASTICSEARCH_USERNAME", "")
    ELASTICSEARCH_PASSWORD: str = os.getenv("ELASTICSEARCH_PASSWORD", "")
    NEWS_INDEX: str = os.getenv("NEWS_INDEX", "news")
    
    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost",
        "http://localhost:8080",
        "http://localhost:3000",
    ]
    
    # Scraper settings
    ENABLE_NEWS_SCRAPER: bool = os.getenv("ENABLE_NEWS_SCRAPER", "False") == "True"
    SCRAPER_INTERVAL_MINUTES: int = int(os.getenv("SCRAPER_INTERVAL_MINUTES", "5"))
    SCRAPER_VERIFY_SSL: bool = os.getenv("SCRAPER_VERIFY_SSL", "True") == "True"
    
    # Claude API settings
    CLAUDE_API_KEY: str = os.getenv("CLAUDE_API_KEY", "")
    CLAUDE_API_URL: str = os.getenv("CLAUDE_API_URL", "https://api.anthropic.com/v1/messages")
    CLAUDE_MODEL: str = os.getenv("CLAUDE_MODEL", "claude-3-5-sonnet-20240307")
    ENABLE_AUTO_SUMMARIZATION: bool = os.getenv("ENABLE_AUTO_SUMMARIZATION", "False") == "True"
    SUMMARY_MAX_LENGTH: int = int(os.getenv("SUMMARY_MAX_LENGTH", "150"))

# Load environment variables manually
def load_env_file(env_file=".env"):
    if os.path.isfile(env_file):
        with open(env_file) as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#') or '=' not in line:
                    continue
                key, value = line.split('=', 1)
                os.environ.setdefault(key, value)

# Try to load from .env file
load_env_file()

# Create settings instance
settings = Settings()