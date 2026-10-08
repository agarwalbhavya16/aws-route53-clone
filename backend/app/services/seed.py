import secrets

from sqlalchemy import select
from sqlalchemy.orm import Session

from ..models import DNSRecord, HostedZone, User


def seed_demo_data(db: Session) -> None:
    if not db.scalar(select(User).where(User.username == "demo")):
        db.add(User(username="demo", display_name="Demo User"))

    if db.scalar(select(HostedZone)):
        db.commit()
        return

    examples = [
        ("example.com", "Public", "Primary public hosted zone for example.com"),
        ("acme.internal", "Private", "Internal application DNS"),
        ("shopnest.app", "Public", "ShopNest production DNS"),
    ]

    for name, zone_type, comment in examples:
        zone = HostedZone(
            name=name,
            zone_id="Z" + secrets.token_hex(7).upper(),
            zone_type=zone_type,
            comment=comment,
        )
        db.add(zone)
        db.flush()

        records = [
            DNSRecord(zone_id=zone.id, name=name, type="A", ttl=300, value="192.0.2.10"),
            DNSRecord(
                zone_id=zone.id,
                name=f"www.{name}",
                type="CNAME",
                ttl=300,
                value=name,
            ),
            DNSRecord(
                zone_id=zone.id,
                name=name,
                type="MX",
                ttl=3600,
                value=f"10 mail.{name}",
            ),
            DNSRecord(
                zone_id=zone.id,
                name=name,
                type="TXT",
                ttl=300,
                value='"v=spf1 include:example.net ~all"',
            ),
        ]
        if name == "acme.internal":
            records[0].value = "10.0.0.20"

        db.add_all(records)
        zone.record_count = len(records)

    db.commit()
