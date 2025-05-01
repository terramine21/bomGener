#обработка запросов, не более

from fastapi import UploadFile, File, Depends, APIRouter, HTTPException
# from fastapi.responses import StreamingResponse
#
# from services import bom_parser, pe3_generator
# import models
from db.session import get_session
# from db import  crud
# import os
#
# from io import BytesIO
#
#

from models.models import BOMEntry, BOMUpload

router = APIRouter()
@router.get("/keke")
async def keke():
    return {"message": "keke"}

# создаем некую запись в базу данных

@router.post("/test-relations")
async def test_relations(session=Depends(get_session)):
    # Создаем upload
    upload = BOMUpload(filename="test.xlsx")
    session.add(upload)
    session.commit()

    # Создаем связанную запись
    entry = BOMEntry(
        designator="R1",
        component_type="Резистор",
        ad_class="R",
        ad_bom="10k",
        quantity=2,
        upload_id=upload.id
    )
    session.add(entry)
    session.commit()

    return {"status": "success"}


#
#
# @router.post("/upload-bom/")
# async def upload_bom(
#         mfile: UploadFile = File(...),
#         db = Depends(get_session)
# ):
#     # Сначала создаем запись о загрузке
#     db_upload = models.BOMUpload(filename=mfile.filename)
#     db.add(db_upload)
#     db.commit()
#     db.refresh(db_upload)
#
#     # Парсим и сохраняем BOM
#     file_path = f"temp_{mfile.filename}"
#     with open(file_path, "wb") as buffer:
#         buffer.write(mfile.file.read())
#
#     bom_data = bom_parser.parse_altium_bom(file_path)
#
#     for entry in bom_data:
#         crud.create_bom_entry(db, entry, upload_id=db_upload.id)
#
#     os.remove(file_path)
#
#     return {"message": f"BOM загружен, ID: {db_upload.id}"}
#
#
# @router.get("/download-pe3/")
# async def download_pe3(db = Depends(get_session)):
#     try:
#         # Получаем данные из БД
#         last_entries = db.query(models.BOMEntry).order_by(models.BOMEntry.id.desc()).all()
#         if not last_entries:
#             raise HTTPException(status_code=404, detail="Нет данных для генерации ПЭ3")
#
#         # Генерируем файл
#         excel_file = pe3_generator.generate_pe3(last_entries)
#
#         # Создаем временный файл для проверки (опционально)
#         with open("debug_pe3.xlsx", "wb") as f:
#             f.write(excel_file.getvalue())
#
#         # Возвращаем файл как поток
#         return StreamingResponse(
#             BytesIO(excel_file.getvalue()),
#             media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
#             headers={
#                 "Content-Disposition": "attachment; filename=ПЭ3.xlsx",
#                 "Content-Length": str(len(excel_file.getvalue()))
#             }
#         )
#     except Exception as e:
#         print(f"Ошибка при генерации файла: {str(e)}")
#         raise HTTPException(status_code=500, detail=str(e))
#

# @router.get("/exel/")
# async def exel(db: Session = Depends(get_db)):
#     new_path =
#
#     return {"message": f"{new_path}"}