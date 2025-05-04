from fastapi import Depends, HTTPException, APIRouter, UploadFile, File
from sqlmodel import Session, select

from models.models import DemoRecord, Upload
from db.session import get_session
from services.bom_parser import parse_uploaded_bom
from services.genExel import generate_excel_for_upload
from schemas.schemas import DemoRecordRead


router = APIRouter(prefix="/BOM", tags=["BOM Operations"])


@router.post("/upload", response_model=list[dict])
async def upload_bom_file(
        file: UploadFile = File(...),
        session: Session = Depends(get_session)
):
    """
    Загружает BOM-файл и сохраняет данные в базу данных.
    Принимает:
    - Excel-файл с перечнем компонентов
    Возвращает:
    - Список элементов
    """
    try:
        bom_data = await parse_uploaded_bom(file)

        upload = Upload(filename=file.filename)
        session.add(upload)
        session.commit()
        session.refresh(upload)

        session.add_all([
            DemoRecord(upload_id=upload.id, **item)
            for item in bom_data
        ])
        session.commit()

        return [{"upload_id": upload.id, **item} for item in bom_data]

    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=f"Ошибка обработки файла: {str(e)}")

# Добавим эндпоинты для получения данных по upload_id
@router.get("/uploads/", response_model=list[int])
def list_uploads(session: Session = Depends(get_session)):
    uploads = session.exec(select(Upload.id)).all()
    return uploads

@router.get("/upload/{upload_id}", response_model=list[DemoRecordRead])
def get_upload_records(
    upload_id: int,
    session: Session = Depends(get_session)
):
    records = session.exec(
        select(DemoRecord)
        .where(DemoRecord.upload_id == upload_id)
    ).all()
    if not records:
        raise HTTPException(status_code=404, detail="Upload not found")
    return records

@router.get("/download/{upload_id}")
def download_upload_as_excel(
    upload_id: int,
    session: Session = Depends(get_session)
):
    """
    Генерирует и возвращает Excel файл с данными загрузки
    """
    return generate_excel_for_upload(upload_id, session)