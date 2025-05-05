from fastapi import FastAPI

from contextlib import asynccontextmanager
from app.db.database import init_db
from app.routes import url
from auth.url import router as auth_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(auth_router)
app.include_router(url.router)