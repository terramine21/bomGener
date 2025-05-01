from sqlalchemy import Column, Integer, String, ForeignKey
from db.database import Base


class BOMEntry(Base): # эдакая структура объекта в базе данных
    __tablename__ = "bom_entries"
    id = Column(Integer, primary_key=True, index=True)
    designator = Column(String)  # "R1, R2"
    component_type = Column(String)  # "Резистор"
    ad_bom = Column(String)  # "RES 10k 0805"
    quantity = Column(Integer)
    upload_id = Column(Integer, ForeignKey("bom_uploads.id")) # id, номер загрузки
