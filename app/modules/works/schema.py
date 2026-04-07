import uuid
from pydantic import BaseModel, ConfigDict


class WorkCreate(BaseModel):
    name: str
    description: str | None = None
    address: str | None = None
    region: str | None = None
    city: str | None = None
    state: str | None = None
    budget: str | None = None
    status: str | None = "ativa"
    image_url: str | None = None


class WorkResponse(BaseModel):
    id: uuid.UUID
    name: str
    description: str | None = None
    address: str | None = None
    region: str | None = None
    city: str | None = None
    state: str | None = None
    budget: str | None = None
    status: str
    image_url: str | None = None

    model_config = ConfigDict(from_attributes=True)
