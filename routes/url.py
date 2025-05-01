#обработка запросов, не более

from fastapi import UploadFile, File, Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import StreamingResponse
from services import bom_parser, pe3_generator
from db.database import SessionLocal
import models
from db import crud
import os


router = APIRouter()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/upload-bom/")
async def upload_bom(
        mfile: UploadFile = File(...),
        db: Session = Depends(get_db)
):
    # Сначала создаем запись о загрузке
    db_upload = models.BOMUpload(filename=mfile.filename)
    db.add(db_upload)
    db.commit()
    db.refresh(db_upload)

    # Парсим и сохраняем BOM
    file_path = f"temp_{mfile.filename}"
    with open(file_path, "wb") as buffer:
        buffer.write(mfile.file.read())

    bom_data = bom_parser.parse_altium_bom(file_path)

    for entry in bom_data:
        crud.create_bom_entry(db, entry, upload_id=db_upload.id)

    os.remove(file_path)

    return {"message": f"BOM загружен, ID: {db_upload.id}"}


@router.get("/download-pe3/")
async def download_pe3(db: Session = Depends(get_db)):
    try:
        # Получаем данные из БД
        last_entries = db.query(models.BOMEntry).order_by(models.BOMEntry.id.desc()).all()
        if not last_entries:
            raise HTTPException(status_code=404, detail="Нет данных для генерации ПЭ3")

        # Генерируем файл
        excel_file = pe3_generator.generate_pe3(last_entries)

        # Создаем временный файл для проверки (опционально)
        with open("debug_pe3.xlsx", "wb") as f:
            f.write(excel_file.getvalue())

        # Возвращаем файл как поток
        return StreamingResponse(
            BytesIO(excel_file.getvalue()),
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={
                "Content-Disposition": "attachment; filename=ПЭ3.xlsx",
                "Content-Length": str(len(excel_file.getvalue()))
            }
        )
    except Exception as e:
        print(f"Ошибка при генерации файла: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

