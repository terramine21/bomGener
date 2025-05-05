"""Ссылки для аутентификации и регистрации пользователей."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlmodel import select

from app.db.session import get_session
from auth.schemas import UserCreate, UserLogin, Token, UserRead
from auth.models import User
from auth.services import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserRead)
def register(user_create: UserCreate, session: Session = Depends(get_session)):
    """
    Регистрация нового пользователя.
    """
    user_exists = session.exec(select(User).where(User.username == user_create.username)).first()
    if user_exists:
        raise HTTPException(status_code=400, detail="Username already registered")
    user = User(username=user_create.username, password_hash=hash_password(user_create.password))
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@router.post("/login", response_model=Token)
def login(user_login: UserLogin, session: Session = Depends(get_session)):
    """Получение JWT токена пользователя"""
    user = session.exec(select(User).where(User.username == user_login.username)).first()
    if not user or not verify_password(user_login.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    token = create_access_token(data={"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}
