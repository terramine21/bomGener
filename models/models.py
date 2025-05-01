from sqlmodel import SQLModel, Field
from typing import Optional

class DemoRecord(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    request_number: int  # Нумерация запросов
    mstr: str           # Строковое значение
    mint: int           # Числовое значение