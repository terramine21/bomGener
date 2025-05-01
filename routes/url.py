from fastapi import Depends, HTTPException, APIRouter
from sqlmodel import Session, select
from models.models import DemoRecord
from schemas.schemas import DemoRecordCreate, DemoRecordRead
from dependencies import get_request_counter
from db.session import get_session

router = APIRouter(prefix="/demo", tags=["Demo Records"])

@router.post("/", response_model=DemoRecordRead)
def create_record(
        record: DemoRecordCreate,
        session: Session = Depends(get_session),
        request_number: int = Depends(get_request_counter)
):
    db_record = DemoRecord(
        request_number=request_number,
        mstr=record.mstr,
        mint=record.mint
    )

    session.add(db_record)
    session.commit()
    session.refresh(db_record)
    return db_record

@router.get("/{record_id}", response_model=DemoRecordRead)
def read_record(
        record_id: int,
        session: Session = Depends(get_session)
):
    record = session.get(DemoRecord, record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    return record

@router.get("/", response_model=list[DemoRecordRead])
def read_all_records(session: Session = Depends(get_session)):
    records = session.exec(select(DemoRecord)).all()
    return records