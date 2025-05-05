from fastapi import Request, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .services import verify_token
from .models import User

# Создаем объект для извлечения токена из заголовков
bearer = HTTPBearer()

def get_current_user(authorization: HTTPAuthorizationCredentials = Depends(bearer)) -> User:
    token = authorization.credentials  # Извлекаем сам токен
    payload = verify_token(token)  # Верификация токена
    user = User(username=payload["sub"])  # Извлечение данных пользователя из токена
    return user