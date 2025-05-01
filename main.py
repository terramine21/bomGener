from fastapi import FastAPI

import models
from routes import url
from db.database import engine

models.Base.metadata.create_all(bind=engine) # создаём все таблицы в базе данных SQLite

app = FastAPI()


app = FastAPI()
app.include_router(url.router)

