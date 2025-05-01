from sqlalchemy import Column, Integer, String, ForeignKey
from db.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    hashed_password = Column(String)

class BOMEntry(Base):
    __tablename__ = "bom_entries"
    id = Column(Integer, primary_key=True, index=True)
    designator = Column(String)  # "R1, R2"
    component_type = Column(String)  # "Резистор"
    ad_class = Column(String)  # "R"
    ad_bom = Column(String)  # "RES 10k 0805"
    quantity = Column(Integer)
    upload_id = Column(Integer, ForeignKey("bom_uploads.id"))

class BOMUpload(Base):
    __tablename__ = "bom_uploads"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    filename = Column(String)