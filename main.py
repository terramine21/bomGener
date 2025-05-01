from fastapi import FastAPI
from db.database import engine, init_db
from contextlib import asynccontextmanager
from routes import url

# Счетчик запросов
request_counter = 0


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Инициализация БД при старте
    init_db()
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(url.router)

