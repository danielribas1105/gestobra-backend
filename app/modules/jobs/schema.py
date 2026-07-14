from datetime import datetime
from typing import Optional
import uuid
from pydantic import BaseModel, ConfigDict

from app.modules.jobs.model import JobStatus, ValueType


class JobCreate(BaseModel):
    statement_id: Optional[uuid.UUID] = None
    origin_id: uuid.UUID
    destiny_id: uuid.UUID
    material_id: uuid.UUID
    quantity: float
    unit: Optional[str] = None
    value_type: ValueType = ValueType.PER_QUANTITY
    rate: float
    value: float
    car_id: uuid.UUID
    carrier_id: uuid.UUID
    driver_id: uuid.UUID
    status: JobStatus = JobStatus.PENDING


class JobUpdate(BaseModel):
    statement_id: Optional[uuid.UUID] = None
    material_id: Optional[uuid.UUID] = None
    quantity: Optional[float] = None
    unit: Optional[str] = None
    value_type: Optional[ValueType] = None
    rate: Optional[float] = None
    value: Optional[float] = None
    driver_id: Optional[uuid.UUID] = None
    car_id: Optional[uuid.UUID] = None
    status: Optional[JobStatus] = None


class JobResponse(BaseModel):
    id: uuid.UUID
    statement_id: Optional[uuid.UUID] = None
    origin_id: uuid.UUID
    destiny_id: uuid.UUID
    material_id: uuid.UUID
    quantity: float
    unit: Optional[str] = None
    value_type: Optional[str] = None
    rate: float
    value: float
    car_id: uuid.UUID
    carrier_id: uuid.UUID
    created_by: uuid.UUID
    driver_id: uuid.UUID
    status: Optional[str] = None
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    # Campos resolvidos
    statement_code: Optional[str] = None
    material_name: Optional[str] = None
    origin_name: Optional[str] = None
    destiny_name: Optional[str] = None
    car_license: Optional[str] = None
    carrier_name: Optional[str] = None
    driver_name: Optional[str] = None
    creator_name: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class JobsCount(BaseModel):
    concluded: int
    in_progress: int
    pending: int
    canceled: int
