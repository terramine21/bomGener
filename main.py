#делаем фигню, что взамен перечня в эксель табличке выплёвывает спецификацию
from fastapi import FastAPI
from db_dataBase.dataBase import init_db
from routes import url

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield
    print("Shutting down...")

app = FastAPI()
app.include_router(url.router)
