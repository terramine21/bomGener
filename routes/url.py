#обработка запросов, не более

from fastapi import UploadFile, File, Depends, APIRouter
from sqlalchemy.orm import Session
from services import bom_parser
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
