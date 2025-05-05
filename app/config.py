"""Настройки конфигурации приложения через переменные окружения."""

from pydantic_settings import BaseSettings
from pydantic import Field, SecretStr

class Settings(BaseSettings):
    """Конфигурация приложения."""

    # Обязательные переменные (вызовут ошибку, если не заданы)
    DB_URL: str = Field(default="sqlite:///bom.db", env="DB_URL")
    SECRET_KEY: SecretStr = Field(..., env="SECRET_KEY")  # Обязательное поле

    # Опциональные (имеют значения по умолчанию)
    ALGORITHM: str = Field(default="HS256", env="ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30, env="ACCESS_TOKEN_EXPIRE_MINUTES")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()