from datetime import datetime
from typing import Optional
import uuid
from pydantic import BaseModel, ConfigDict

from app.modules.jobs.model import JobStatus


class JobCreate(BaseModel):
    statement_id: Optional[uuid.UUID] = None
    origin: uuid.UUID
    destiny: uuid.UUID
    car_id: uuid.UUID
    driver_id: uuid.UUID
    status: JobStatus = JobStatus.PENDING


class JobUpdate(BaseModel):
    statement_id: Optional[uuid.UUID] = None
    driver_id: Optional[uuid.UUID] = None
    car_id: Optional[uuid.UUID] = None
    status: Optional[JobStatus] = None


class JobResponse(BaseModel):
    id: uuid.UUID
    statement_id: Optional[uuid.UUID] = None
    origin: uuid.UUID
    destiny: uuid.UUID
    car_id: uuid.UUID
    created_by: uuid.UUID
    driver_id: uuid.UUID
    status: Optional[str] = None
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    # Campos resolvidos
    statement_code: Optional[str] = None
    material_name: Optional[str] = None
    m3: Optional[int] = None
    value_m3: Optional[float] = None
    origin_name: Optional[str] = None
    destiny_name: Optional[str] = None
    car_license: Optional[str] = None
    driver_name: Optional[str] = None
    creator_name: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
