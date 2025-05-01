from sqlmodel import SQLModel

class Settings:
    DB_URL: str = "sqlite:///demo.db"

settings = Settings()