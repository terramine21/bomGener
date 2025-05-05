"""Pydantic-схемы для операций с пользователями и токенами."""

from pydantic import BaseModel

class UserCreate(BaseModel):
    """Схема создания нового пользователя."""
    username: str
    password: str

class UserRead(BaseModel):
    """Схема чтения данных пользователя."""
    id: int
    username: str

    class Config:
        """Конфигурация для поддержки ORM-моделей."""
        from_attributes = True

class UserLogin(BaseModel):
    """Схема входа пользователя."""
    username: str
    password: str

class Token(BaseModel):
    """Схема токена доступа."""
    access_token: str
    token_type: str
