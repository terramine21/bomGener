#обработка запросов, не более

from fastapi import Request, HTTPException, APIRouter, Depends
from  fastapi.responses import RedirectResponse

router = APIRouter()

@router.post("/test1")
def test1(data: str):
    return {"message": data}

@router.get("/{tested1}")
def tested1():
    return "tested1"
