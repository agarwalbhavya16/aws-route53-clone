import secrets

from fastapi import HTTPException
from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from ..models import HostedZone
from ..schemas import ZoneIn
from ..utils.validation import VALID_ZONE_TYPES, validate_domain_name


def list_zones(db: Session, search: str) -> list[HostedZone]:
    query = select(HostedZone).order_by(HostedZone.name)
    if search.strip():
        query = query.where(
            or_(
                HostedZone.name.ilike(f"%{search}%"),
                HostedZone.zone_id.ilike(f"%{search}%"),
                HostedZone.comment.ilike(f"%{search}%"),
            )
        )
    return list(db.scalars(query).all())


def create_zone(db: Session, body: ZoneIn) -> HostedZone:
    try:
        name = validate_domain_name(body.name)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    if body.zone_type not in VALID_ZONE_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Hosted zone type must be Public or Private",
        )

    duplicate = db.scalar(
        select(HostedZone).where(func.lower(HostedZone.name) == name)
    )
    if duplicate:
        raise HTTPException(
            status_code=409,
            detail="A hosted zone with this name already exists",
        )

    zone = HostedZone(
        name=name,
        zone_id="Z" + secrets.token_hex(7).upper(),
        zone_type=body.zone_type,
        comment=body.comment.strip(),
    )
    db.add(zone)
    db.commit()
    db.refresh(zone)
    return zone


def update_zone(db: Session, zone_id: int, body: ZoneIn) -> HostedZone:
    zone = db.get(HostedZone, zone_id)
    if not zone:
        raise HTTPException(status_code=404, detail="Hosted zone not found")

    try:
        name = validate_domain_name(body.name)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    if body.zone_type not in VALID_ZONE_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Hosted zone type must be Public or Private",
        )

    duplicate = db.scalar(
        select(HostedZone).where(
            func.lower(HostedZone.name) == name,
            HostedZone.id != zone_id,
        )
    )
    if duplicate:
        raise HTTPException(
            status_code=409,
            detail="A hosted zone with this name already exists",
        )

    zone.name = name
    zone.zone_type = body.zone_type
    zone.comment = body.comment.strip()
    db.commit()
    db.refresh(zone)
    return zone


def delete_zone(db: Session, zone_id: int) -> None:
    zone = db.get(HostedZone, zone_id)
    if not zone:
        raise HTTPException(status_code=404, detail="Hosted zone not found")
    db.delete(zone)
    db.commit()
