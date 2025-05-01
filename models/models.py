from sqlmodel import SQLModel, Field
from typing import Optional

class DemoRecord(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    mstr: str           # Строковое значение
    mint: int           # Числовое значение