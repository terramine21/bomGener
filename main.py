from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from . import models, schemas, crud
from db.database import SessionLocal, engine
from .services import bom_parser, pe3_generator
import os

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/upload-bom/")
async def upload_bom(
        file: UploadFile = File(...),
        db: Session = Depends(get_db)
):
    # Сохраняем файл временно
    file_path = f"temp_{file.filename}"
    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())

    # Парсим BOM
    bom_data = bom_parser.parse_altium_bom(file_path)

    # Генерируем ПЭ3
    pe3_path = "pe3_output.xlsx"
    pe3_generator.generate_pe3(bom_data, pe3_path)

    # Удаляем временный файл
    os.remove(file_path)

    return {"message": "ПЭ3 сгенерирован", "path": pe3_path}