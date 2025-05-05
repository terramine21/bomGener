"""Утилиты для работы с паролями и JWT-токенами."""

from typing import Optional
from datetime import timedelta, datetime

import jwt
from fastapi import HTTPException
from passlib.context import CryptContext

from app.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def hash_password(password: str) -> str:
    """Хеширует пароль с использованием bcrypt."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Сравнивает обычный и хешированный пароли."""
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    """Создает JWT токен с заданным сроком действия."""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({"exp": expire})
    return jwt.encode(
        to_encode,
        settings.SECRET_KEY.get_secret_value(),  # Достаём значение SecretStr
        algorithm=settings.ALGORITHM
    )


def verify_token(token: str) -> dict:
    """
    Проверяет подлинность и срок действия JWT токена.

    Возвращает полезную нагрузку, если токен валиден.
    Генерирует HTTPException в противном случае.
    """
    try:
        if not token:
            raise HTTPException(status_code=401, detail="Token is missing")

        # Используем get_secret_value() для преобразования SecretStr в строку
        decoded_token = jwt.decode(
            token,
            settings.SECRET_KEY.get_secret_value(),  # <-- Вот это исправление
            algorithms=[settings.ALGORITHM]
        )

        exp = decoded_token.get("exp")
        if exp and datetime.utcfromtimestamp(exp) < datetime.utcnow():
            raise HTTPException(status_code=401, detail="Token expired")

        return decoded_token
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.PyJWTError as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")