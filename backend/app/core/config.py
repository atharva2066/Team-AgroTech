# app/core/config.py

from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List, Optional


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    MONGO_URL: Optional[str] = None
    DATABASE_NAME: str = "agrochar_db"
    JWT_SECRET: Optional[str] = None
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:5500",
    ]


settings = Settings()

# Force validation manually

if not settings.JWT_SECRET:
    raise ValueError("JWT_SECRET not set in environment")