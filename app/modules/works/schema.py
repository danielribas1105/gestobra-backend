from datetime import datetime
from typing import Optional
import uuid
from pydantic import BaseModel, ConfigDict, Field

from app.modules.works.model import WorkStatus


class WorkCreate(BaseModel):
    name: str
    description: str | None = None
    address: str | None = None
    region: str | None = None
    city: str | None = None
    state: str | None = None
    active: bool = Field(default=True)
    status: WorkStatus = WorkStatus.ATIVA
    image: str | None = None


class WorkUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    address: Optional[str] = None
    region: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    active: Optional[bool] = None
    status: Optional[WorkStatus] = None
    image: Optional[str] = None


class WorkResponse(BaseModel):
    id: uuid.UUID
    name: str
    description: Optional[str] = None
    address: Optional[str] = None
    region: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    active: bool
    status: WorkStatus
    image: Optional[str] = None
    created_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)
