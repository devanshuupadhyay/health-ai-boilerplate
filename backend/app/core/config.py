# path: backend/app/core/config.py

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Variables that will be read from the .env file
    DATABASE_URL: str
    SECRET_KEY: str

    # Celery configuration
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/0"

    #  MEILISEARCH SETTINGS ---
    MEILI_URL: str = "http://search:7700"  # Use service name from docker-compose
    MEILI_MASTER_KEY: str = (
        "chnadukechachanechandukichachikochandikechamchesechatnichatai"
    )

    # Sentry DSN
    SENTRY_DSN: Optional[str] = None

    # Variables with default values
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        # This tells pydantic to look for a file named .env
        env_file = ".env"
        extra = "ignore"


# Create a single, importable instance of the settings
settings = Settings()
