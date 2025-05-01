from sqlmodel import create_engine, SQLModel
from models.models import BOMUpload, BOMEntry  # Явный импорт моделей

engine = create_engine("sqlite:///bom.db")

def init_db():
    # Убедитесь, что модели импортированы до этой строки
    SQLModel.metadata.create_all(engine)