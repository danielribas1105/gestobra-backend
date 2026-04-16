from datetime import datetime
from typing import Literal, Optional
import uuid
from pydantic import BaseModel, ConfigDict

from app.modules.jobs.model import JobStatus


class JobCreate(BaseModel):
    statement_id: uuid.UUID
    origin: uuid.UUID
    destiny: uuid.UUID
    car_id: uuid.UUID
    driver_id: uuid.UUID
    status: JobStatus = JobStatus.PENDING


class JobUpdate(BaseModel):
    driver_id: Optional[uuid.UUID] = None
    car_id: Optional[uuid.UUID] = None
    status: Optional[JobStatus] = None


class JobResponse(BaseModel):
    id: uuid.UUID
    statement_id: uuid.UUID
    origin: uuid.UUID
    destiny: uuid.UUID
    car_id: uuid.UUID
    driver_id: uuid.UUID
    created_by: uuid.UUID
    status: JobStatus
    created_at: datetime | None = None
    updated_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)
