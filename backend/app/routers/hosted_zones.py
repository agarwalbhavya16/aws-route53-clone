from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import User
from ..schemas import ZoneIn, ZoneOut
from ..services.auth import get_current_user
from ..services.hosted_zones import create_zone, delete_zone, list_zones, update_zone

router = APIRouter(prefix="/api/hosted-zones", tags=["Hosted Zones"])


@router.get("", response_model=list[ZoneOut])
def get_zones(
    search: str = "",
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return list_zones(db, search)


@router.post("", response_model=ZoneOut, status_code=201)
def post_zone(
    body: ZoneIn,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return create_zone(db, body)


@router.put("/{zone_id}", response_model=ZoneOut)
def put_zone(
    zone_id: int,
    body: ZoneIn,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return update_zone(db, zone_id, body)


@router.delete("/{zone_id}")
def remove_zone(
    zone_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    delete_zone(db, zone_id)
    return {"ok": True}
