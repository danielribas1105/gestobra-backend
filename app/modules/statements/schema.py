from datetime import datetime
import uuid
from pydantic import BaseModel, ConfigDict


class StatementCreate(BaseModel):
    job_id: uuid.UUID
    status: str


class StatementUpdate(BaseModel):
    status: str


class StatementResponse(BaseModel):
    id: uuid.UUID
    job_id: uuid.UUID
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
