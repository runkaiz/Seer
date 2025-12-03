"""
Configuration management for the Anime Recommendation API.

Author: Runkai Zhang
"""

from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # API Keys (Required)
    openai_api_key: str
    mal_client_id: str

    # Application
    app_name: str = "Anime Recommendation API"
    debug: bool = False

    # CORS
    allowed_origins: list[str] = ["http://localhost:5173", "http://localhost:3000"]

    # OpenAI Settings
    openai_model: str = "gpt-5-thinking"
    max_candidates: int = 10

    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
