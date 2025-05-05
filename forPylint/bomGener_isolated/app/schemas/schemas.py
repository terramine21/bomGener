"""Модели схем данных для загрузки и обработки записей BOM."""

from typing import Optional
from pydantic import BaseModel, model_validator


class UploadRead(BaseModel):
    """Схема для представления информации о загрузке."""
    id: int
    filename: str
    project_name: str

class DemoRecordCreate(BaseModel):
    """Схема для создания новой записи DemoRecord."""
    designator: str
    ad_bom: str
    ad_class: str
    ad_note: str
    ad_ss: str
    quantity: int

class DemoRecordRead(BaseModel):
    """Схема для чтения записи DemoRecord."""
    upload_id: int
    id: int                 # id элемента внутри списка
    designator: str
    ad_bom: str
    ad_class: str
    ad_note: str
    ad_ss: str
    quantity: int

class DemoRecordUpdate(BaseModel):
    """Схема для обновления записи DemoRecord."""
    designator: Optional[str] = None
    ad_bom: Optional[str] = None
    ad_class: Optional[str] = None
    ad_note: Optional[str] = None
    ad_ss: Optional[str] = None
    quantity: Optional[int] = None

    # необходимо расширить
    @model_validator(mode='before')
    def check_quantity(cls, values):
        """Проверяет, что значение quantity неотрицательно."""
        if 'quantity' in values and values['quantity'] is not None and values['quantity'] < 0:
            raise ValueError("Quantity must be greater than or equal to 0")
        return values
