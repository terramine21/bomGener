#описание входных и выходных параметров(?)
from pydantic import BaseModel

class BOMEntryCreate(BaseModel):
    designator: str
    component_type: str
    ad_class: str
    ad_bom: str
    quantity: int