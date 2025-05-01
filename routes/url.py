#обработка запросов, не более

from fastapi import UploadFile, File, Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import StreamingResponse
from services import bom_parser, pe3_generator
from db.database import SessionLocal
from db import crud


router = APIRouter()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/upload-bom/") #пока тупо загружаем файл и в ответ получаем путь к загруженному файлу
async def upload_bom( # принимаем файл, и ??
        mfile: UploadFile = File(...),
        db: Session = Depends(get_db)
):
    # Сохраняем файл временно
    file_path = f"temp_{mfile.filename}"
    with open(file_path, "wb") as buffer:
        buffer.write(mfile.file.read())

    # Парсим BOM

    bom_data = bom_parser.parse_altium_bom(file_path)
    # Добавляем данные в БД
    for entry in bom_data:
        crud.create_bom_entry(db, entry) #тут уже встроен db.commit и прочее

    return {"message": mfile.filename}


@router.get("/download-pe3/")
async def download_pe3(db: Session = Depends(get_db)):

    # Получаем последние данные из БД
    last_entries = crud.get_last_bom_entry(db)
    if not last_entries:
        raise HTTPException(
            status_code=404,
            detail="Нет данных для генерации ПЭ3. Сначала загрузите BOM."
        )

    # Генерируем Excel-файл в памяти
    try:
        excel_file = pe3_generator.generate_pe3([last_entries])  # Передаем список с одним элементом
        excel_file.seek(0)  # Перемещаем указатель в начало файла
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка генерации файла: {str(e)}"
        )
    # Возвращаем файл как поток
    return StreamingResponse(
        excel_file,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={
            "Content-Disposition": "attachment; filename=ПЭ3.xlsx",
            "Content-Type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        }
    )