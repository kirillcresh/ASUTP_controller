from pathlib import Path

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    """Settings for env file"""
    SERVER_HOST: str = "localhost"
    SERVER_PORT: int = 8000
    CORS_ALLOWED_ORIGINS: str
    PATH_LOG_DIR: Path
    PATH_LOG_DIR: str

    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE: int = 3600
    REFRESH_TOKEN_EXPIRE: int = 2592000

    POSTGRES_HOST: str
    POSTGRES_USER: str
    POSTGRES_DB: str
    POSTGRES_PASSWORD: str
    POSTGRES_PORT: int


settings = Settings(
    _env_file=".env",
    _env_file_encoding="utf-8"
)
