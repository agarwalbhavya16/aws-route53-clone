from pydantic import BaseModel, ConfigDict, Field


class LoginIn(BaseModel):
    username: str
    password: str


class ZoneIn(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    zone_type: str = "Public"
    comment: str = Field(default="", max_length=500)


class ZoneOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    zone_id: str
    zone_type: str
    comment: str
    record_count: int


class RecordIn(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    type: str
    ttl: int = Field(default=300, ge=0, le=86400)
    value: str = Field(min_length=1, max_length=4096)
    routing_policy: str = "Simple"


class RecordOut(RecordIn):
    model_config = ConfigDict(from_attributes=True)

    id: int
