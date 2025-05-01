from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from datetime import datetime


class BOMUploadBase(SQLModel):
    filename: str


class BOMUpload(BOMUploadBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    uploaded_at: datetime = Field(default_factory=datetime.now)

    # Важно: связь должна использовать точное имя класса
    entries: List["BOMEntry"] = Relationship(back_populates="upload")


class BOMEntryBase(SQLModel):
    designator: str
    component_type: str
    ad_class: str
    ad_bom: str
    quantity: int
    upload_id: Optional[int] = Field(default=None, foreign_key="bom_uploads.id")


class BOMEntry(BOMEntryBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    # Связь с явным указанием foreign_key
    upload: Optional[BOMUpload] = Relationship(back_populates="entries")