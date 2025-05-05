"""Настройки конфигурации приложения через переменные окружения."""

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Конфигурация приложения, загружаемая из .env файла или переменных окружения."""

    DB_URL: str = "sqlite:///bom.db"
    SECRET_KEY: str = "Admin"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        """Настройки для Pydantic — указывает путь к файлу .env."""
        env_file = ".env"

settings = Settings()
