from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import Optional
import models

def create_bom_entry(db: Session, entry: dict):
    db_entry = models.BOMEntry(
        designator=entry["designator"],
        component_type=entry["ad_class"],
        ad_bom=entry["ad_bom"],
        quantity=entry["quantity"]
    )
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    return db_entry


def get_last_bom_entry(db: Session) -> Optional[models.BOMEntry]:
    return db.query(models.BOMEntry) \
        .order_by(desc(models.BOMEntry.id)) \
        .first()