from fastapi import HTTPException
from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from ..models import DNSRecord, HostedZone
from ..schemas import RecordIn
from ..utils.validation import normalize_record_name, normalize_record_value, validate_record_type


def get_zone_or_404(db: Session, zone_id: int) -> HostedZone:
    zone = db.get(HostedZone, zone_id)
    if not zone:
        raise HTTPException(status_code=404, detail="Hosted zone not found")
    return zone


def list_records(
    db: Session,
    zone_id: int,
    search: str,
    record_type: str,
    page: int,
    page_size: int,
):
    get_zone_or_404(db, zone_id)

    page = max(1, page)
    page_size = min(max(1, page_size), 50)

    query = (
        select(DNSRecord)
        .where(DNSRecord.zone_id == zone_id)
        .order_by(DNSRecord.name, DNSRecord.type)
    )
    if search.strip():
        query = query.where(
            or_(
                DNSRecord.name.ilike(f"%{search}%"),
                DNSRecord.value.ilike(f"%{search}%"),
            )
        )
    if record_type and record_type != "All":
        query = query.where(DNSRecord.type == record_type)

    total = db.scalar(select(func.count()).select_from(query.subquery())) or 0
    items = list(
        db.scalars(query.offset((page - 1) * page_size).limit(page_size)).all()
    )
    pages = max(1, (total + page_size - 1) // page_size)

    return {
        "items": items,
        "total": total,
        "page": page,
        "page_size": page_size,
        "pages": pages,
    }


def create_record(db: Session, zone_id: int, body: RecordIn) -> DNSRecord:
    zone = get_zone_or_404(db, zone_id)

    try:
        record_type = validate_record_type(body.type)
        name = normalize_record_name(body.name)
        value = normalize_record_value(body.value)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    record = DNSRecord(
        zone_id=zone_id,
        name=name,
        type=record_type,
        ttl=body.ttl,
        value=value,
        routing_policy=body.routing_policy.strip() or "Simple",
    )
    db.add(record)
    zone.record_count = (zone.record_count or 0) + 1
    db.commit()
    db.refresh(record)
    return record


def update_record(
    db: Session,
    zone_id: int,
    record_id: int,
    body: RecordIn,
) -> DNSRecord:
    get_zone_or_404(db, zone_id)
    record = db.scalar(
        select(DNSRecord).where(
            DNSRecord.id == record_id,
            DNSRecord.zone_id == zone_id,
        )
    )
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")

    try:
        record_type = validate_record_type(body.type)
        name = normalize_record_name(body.name)
        value = normalize_record_value(body.value)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    record.name = name
    record.type = record_type
    record.ttl = body.ttl
    record.value = value
    record.routing_policy = body.routing_policy.strip() or "Simple"
    db.commit()
    db.refresh(record)
    return record


def delete_record(db: Session, zone_id: int, record_id: int) -> None:
    record = db.scalar(
        select(DNSRecord).where(
            DNSRecord.id == record_id,
            DNSRecord.zone_id == zone_id,
        )
    )
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")

    zone = db.get(HostedZone, zone_id)
    db.delete(record)
    if zone:
        zone.record_count = max(0, (zone.record_count or 1) - 1)
    db.commit()
