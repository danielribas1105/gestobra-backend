from datetime import datetime
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
    code: str | None = None
    material_id: uuid.UUID | None = None
    m3: int | None = None
    active: bool | None = None
    status: StatementStatus | None = None


class StatementResponse(BaseModel):
    id: uuid.UUID
    code: str
    material_id: uuid.UUID
    m3: int
    active: bool
    status: StatementStatus
    created_at: datetime | None = None
    updated_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)
