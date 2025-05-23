"""Модуль для обработки операций с BOM, таких как: загрузка, список и удаление записей."""

from fastapi import Depends, HTTPException, APIRouter, UploadFile, File, Form
from pydantic import ValidationError
from sqlmodel import Session, select
from sqlalchemy import delete

from app.models import DemoRecord, Upload
from app.db.session import get_session
from app.services.bom_parser import parse_uploaded_bom
from app.services.gen_exel import generate_excel_for_upload
from app.schemas.schemas import DemoRecordRead, UploadRead, DemoRecordUpdate

from auth.dependencies import get_current_user
from auth.schemas import UserRead

router = APIRouter(prefix="/BOM", tags=["BOM Operations"])


@router.post("/upload/new", response_model=list[dict])
async def upload_bom_file(
        file: UploadFile = File(...),
        project_name: str = Form(...),
        session: Session = Depends(get_session),
        current_user: UserRead = Depends(get_current_user)
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

        upload = Upload(filename=file.filename, project_name=project_name)
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


@router.get("/upload/list", response_model=list[UploadRead])
def list_uploads(
    session: Session = Depends(get_session),
    current_user: UserRead = Depends(get_current_user)
):
    """
    Получает список всех загрузок.
    """
    uploads = session.exec(select(Upload)).all()
    return uploads

@router.get("/upload/{upload_id}", response_model=list[DemoRecordRead])
def get_upload_records(
    upload_id: int,
    session: Session = Depends(get_session),
    current_user: UserRead = Depends(get_current_user)
):
    """
    Получает записи для заданной загрузки.
    """
    records = session.exec(
        select(DemoRecord).where(DemoRecord.upload_id == upload_id) #?????
    ).all()
    if not records:
        raise HTTPException(status_code=404, detail="Upload not found")
    return records

@router.get("/download/{upload_id}")
def download_upload_as_excel(
    upload_id: int,
    session: Session = Depends(get_session),
    current_user: UserRead = Depends(get_current_user)
):
    """
    Генерирует и возвращает Excel файл с данными загрузки
    """
    return generate_excel_for_upload(upload_id, session)

@router.delete("/upload/{upload_id}", status_code=204)
def delete_upload(
    upload_id: int,
    session: Session = Depends(get_session),
    current_user: UserRead = Depends(get_current_user)
):
    """
    Удаляет загрузку по указанному ID.
    """
    upload = session.get(Upload, upload_id)
    if not upload:
        raise HTTPException(status_code=404, detail="Загрузка не найдена")

    session.exec(
        delete(DemoRecord).where(DemoRecord.upload_id == upload_id)
    )

    session.delete(upload)
    session.commit()

    return {"message": "Удалено успешно"}

@router.patch("/upload/{upload_id}/record/{record_id}", response_model=DemoRecordRead)
def update_demo_record(
    upload_id: int,
    record_id: int,
    record_update: DemoRecordUpdate,
    session: Session = Depends(get_session),
    current_user: UserRead = Depends(get_current_user)
):
    """
    Обновляет запись DemoRecord по её record_id и upload_id
    """
    try:
        record = session.get(DemoRecord, record_id)

        if not record or record.upload_id != upload_id:
            raise HTTPException(status_code=404, detail="Запись не найдена")

        update_data = record_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(record, key, value)

        session.add(record)
        session.commit()
        session.refresh(record)

        return record

    except ValidationError as e:
        raise HTTPException(status_code=400, detail=f"Ошибка валидации: {e.errors()}")
