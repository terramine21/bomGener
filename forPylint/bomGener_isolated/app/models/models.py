"""Модели для работы с загрузками BOM и элементами записей BOM."""

from typing import Optional, List  # Импорт стандартных библиотек
from sqlmodel import SQLModel, Field, Relationship  # Импорт сторонней библиотеки

class Upload(SQLModel, table=True):
    """Модель для загрузки BOM-файлов."""
    __tablename__ = "upload"

    id: Optional[int] = Field(default=None, primary_key=True)
    project_name: str
    filename: str
    records: List["DemoRecord"] = Relationship(back_populates="upload")


class DemoRecord(SQLModel, table=True):
    """Модель для записи элемента BOM."""
    __tablename__ = "demo_record"

    upload_id: Optional[int] = Field(default=None,
                                     foreign_key="upload.id") # номер в общем листе загрузок
    upload: Optional[Upload] = Relationship(back_populates="records")
    id: Optional[int] = Field(default=None, primary_key=True) # id элементов внутри сохраненного bom
    designator: str # DA2, DA3
    ad_bom: str     # 1432УД30У
    ad_class: str   # Микросхема
    ad_note: str    # НПП "Пульсар"
    ad_ss: str      # АЕЯР.431100.280-18ТУ
    quantity: int   # 2
