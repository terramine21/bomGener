from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from db.database import Base


class BOMUpload(Base):
    __tablename__ = "bom_uploads"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String)
    uploaded_at = Column(DateTime, server_default=func.now())

    # Связь с BOMEntry
    entries = relationship("BOMEntry", back_populates="upload")


class BOMEntry(Base):
    __tablename__ = "bom_entries"
    id = Column(Integer, primary_key=True, index=True)
    designator = Column(String)
    component_type = Column(String)
    ad_class = Column(String)  # Добавлено новое поле
    ad_bom = Column(String)
    quantity = Column(Integer)
    upload_id = Column(Integer, ForeignKey("bom_uploads.id"))

    # Связь с BOMUpload
    upload = relationship("BOMUpload", back_populates="entries")