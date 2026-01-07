"""
Application configuration using Pydantic Settings
"""
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    """Application settings with environment variable support"""

    semantic_scholar_key: str
    embedding_model: str = "all-MiniLM-L6-v2"
    default_top_k: int = 20

    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()