from pydantic import BaseModel, model_validator
from typing import Optional

class UploadRead(BaseModel):
    id: int
    filename: str
    project_name: str

class DemoRecordCreate(BaseModel):
    designator: str
    ad_bom: str
    ad_class: str
    ad_note: str
    ad_ss: str
    quantity: int

class DemoRecordRead(BaseModel):
    upload_id: int
    id: int                 #id элемента внутри списка
    designator: str
    ad_bom: str
    ad_class: str
    ad_note: str
    ad_ss: str
    quantity: int

class DemoRecordUpdate(BaseModel):
    designator: Optional[str] = None
    ad_bom: Optional[str] = None
    ad_class: Optional[str] = None
    ad_note: Optional[str] = None
    ad_ss: Optional[str] = None
    quantity: Optional[int] = None

    @model_validator(mode='before')
    def check_quantity(cls, values):
        if 'quantity' in values and values['quantity'] is not None and values['quantity'] < 0:
            raise ValueError("Quantity must be greater than or equal to 0")
        return values