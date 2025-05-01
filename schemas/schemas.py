from pydantic import BaseModel

class DemoRecordCreate(BaseModel):
    mstr: str
    mint: int

class DemoRecordRead(BaseModel):
    id: int
    mstr: str
    mint: int