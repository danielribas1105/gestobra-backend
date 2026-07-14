from datetime import datetime
from typing import Optional
import uuid
from pydantic import BaseModel, ConfigDict

from app.modules.statements.model import StatementStatus


class StatementCreate(BaseModel):
    code: str
    active: bool = True
    status: StatementStatus = StatementStatus.PENDING


class StatementUpdate(BaseModel):
    code: Optional[str] = None
    active: Optional[bool] = None
    status: Optional[StatementStatus] = None


class StatementResponse(BaseModel):
    id: uuid.UUID
    code: Optional[str] = None
    active: bool
    status: StatementStatus
    created_at: datetime | None = None
    updated_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


class StatementsCount(BaseModel):
    concluded: int
    in_progress: int
    pending: int
    canceled: int
