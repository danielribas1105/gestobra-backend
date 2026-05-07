from datetime import datetime
from typing import Optional
import uuid
from pydantic import BaseModel, ConfigDict

from app.modules.works.model import WorkStatus


class WorkCreate(BaseModel):
    code: str
    name: str
    cnpj: str | None = None
    description: str | None = None
    address: str | None = None
    zip_code: str | None = None
    city: str | None = None
    state: str | None = None
    status: WorkStatus = WorkStatus.ATIVA


class WorkUpdate(BaseModel):
    code: Optional[str] = None
    name: Optional[str] = None
    cnpj: Optional[str] = None
    description: Optional[str] = None
    address: Optional[str] = None
    zip_code: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    status: Optional[WorkStatus] = None


class WorkResponse(BaseModel):
    id: uuid.UUID
    code: str
    name: str
    cnpj: Optional[str] = None
    description: Optional[str] = None
    address: Optional[str] = None
    zip_code: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    status: WorkStatus
    created_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)
