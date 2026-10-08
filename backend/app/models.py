from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    display_name: Mapped[str] = mapped_column(String(160))


class HostedZone(Base):
    __tablename__ = "hosted_zones"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), index=True)
    zone_id: Mapped[str] = mapped_column(String(40), unique=True)
    zone_type: Mapped[str] = mapped_column(String(20), default="Public")
    comment: Mapped[str] = mapped_column(Text, default="")
    record_count: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )

    records: Mapped[list["DNSRecord"]] = relationship(
        back_populates="zone",
        cascade="all, delete-orphan",
    )


class DNSRecord(Base):
    __tablename__ = "dns_records"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    zone_id: Mapped[int] = mapped_column(
        ForeignKey("hosted_zones.id", ondelete="CASCADE"),
        index=True,
    )
    name: Mapped[str] = mapped_column(String(255), index=True)
    type: Mapped[str] = mapped_column(String(10), index=True)
    ttl: Mapped[int] = mapped_column(Integer, default=300)
    value: Mapped[str] = mapped_column(Text)
    routing_policy: Mapped[str] = mapped_column(String(50), default="Simple")

    zone: Mapped[HostedZone] = relationship(back_populates="records")


class SessionToken(Base):
    __tablename__ = "sessions"

    token: Mapped[str] = mapped_column(String(128), primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    expires_at: Mapped[datetime] = mapped_column(DateTime)
