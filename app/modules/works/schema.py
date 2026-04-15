from typing import Optional
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


class WorkUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    address: Optional[str] = None
    region: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    budget: Optional[str] = None
    status: Optional[str] = None
    image_url: Optional[str] = None


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
