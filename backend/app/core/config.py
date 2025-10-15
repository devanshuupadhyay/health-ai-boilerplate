# path: backend/app/core/config.py

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Variables that will be read from the .env file
    DATABASE_URL: str
    SECRET_KEY: str

    # Variables with default values
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        # This tells pydantic to look for a file named .env
        env_file = ".env"


# Create a single, importable instance of the settings
settings = Settings()
