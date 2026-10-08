from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import User
from ..schemas import RecordIn, RecordOut
from ..services.auth import get_current_user
from ..services.records import create_record, delete_record, list_records, update_record

router = APIRouter(prefix="/api/hosted-zones/{zone_id}/records", tags=["DNS Records"])


@router.get("")
def get_records(
    zone_id: int,
    search: str = "",
    record_type: str = "",
    page: int = 1,
    page_size: int = 10,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return list_records(db, zone_id, search, record_type, page, page_size)


@router.post("", response_model=RecordOut, status_code=201)
def post_record(
    zone_id: int,
    body: RecordIn,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return create_record(db, zone_id, body)


@router.put("/{record_id}", response_model=RecordOut)
def put_record(
    zone_id: int,
    record_id: int,
    body: RecordIn,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return update_record(db, zone_id, record_id, body)


@router.delete("/{record_id}")
def remove_record(
    zone_id: int,
    record_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    delete_record(db, zone_id, record_id)
    return {"ok": True}
