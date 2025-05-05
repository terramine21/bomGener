"""Модель пользователя для базы данных."""
from typing import Optional
from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
    """Модель таблицы пользователей."""
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True)
    password_hash: str
