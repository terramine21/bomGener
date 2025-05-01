from fastapi import FastAPI
from db.database import init_db
from routes import url


from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI()

app.include_router(url.router)

