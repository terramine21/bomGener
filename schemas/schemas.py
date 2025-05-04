from pydantic import BaseModel

class UploadRead(BaseModel):
    id: int
    filename: str

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