from fastapi import FastAPI
from db.database import init_db
from contextlib import asynccontextmanager
from routes import url

# Счетчик запросов


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Инициализация БД при старте
    init_db()
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(url.router)


