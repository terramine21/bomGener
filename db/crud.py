# from sqlmodel import Session
# from sqlalchemy import desc
# from typing import Optional
# from models import models
#
#
# def create_bom_entry(db: Session, entry: dict, upload_id: int):
#     db_entry = models.BOMEntry(
#         designator=entry["designator"],
#         component_type=entry["ad_class"],  # Исправлено с ad_class
#         ad_bom=entry["ad_bom"],
#         quantity=entry["quantity"],
#         upload_id=upload_id  # Добавлен upload_id
#     )
#     db.add(db_entry)
#     db.commit()
#     db.refresh(db_entry)
#     return db_entry
#
#
# def get_last_bom_entry(db: Session) -> Optional[models.BOMEntry]:
#     return db.query(models.BOMEntry) \
#         .order_by(desc(models.BOMEntry.id)) \
#         .first()