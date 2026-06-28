"""Application configuration.

Settings are read from environment variables (optionally a local ``.env``
file). See ``.env.example`` for the available knobs.
"""

from __future__ import annotations

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="ASSISTANT_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    database_url: str = "sqlite:///./assistant.db"
    owner_name: str = "Valdimar"

    # When True, WRITE tools execute immediately. When False (default), they
    # are routed through the human-in-the-loop approval workflow.
    auto_approve: bool = False


@lru_cache
def get_settings() -> Settings:
    """Return a cached Settings instance."""
    return Settings()
