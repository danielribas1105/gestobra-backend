from datetime import datetime
from typing import Optional
import uuid
from pydantic import BaseModel, ConfigDict

from app.modules.statements.model import StatementStatus


class StatementCreate(BaseModel):
    code: str
    material_id: uuid.UUID
    m3: int
    active: bool = True
    status: StatementStatus = StatementStatus.PENDING


class StatementUpdate(BaseModel):
    code: Optional[str] = None
    material_id: Optional[uuid.UUID] = None
    m3: Optional[int] = None
    active: Optional[bool] = None
    status: Optional[StatementStatus] = None


class StatementResponse(BaseModel):
    id: uuid.UUID
    code: Optional[str] = None
    material_id: uuid.UUID
    m3: int
    active: bool
    status: StatementStatus
    created_at: datetime | None = None
    updated_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


class StatementsCount(BaseModel):
    approved: int
    pending: int
    rejected: int
    concluded: int
