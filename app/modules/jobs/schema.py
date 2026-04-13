from datetime import datetime
from typing import Literal, Optional
import uuid
from pydantic import BaseModel, ConfigDict


class JobCreate(BaseModel):
    origin: uuid.UUID
    destiny: uuid.UUID
    car_id: uuid.UUID
    driver_id: uuid.UUID
    m3: int
    status: Literal["pending", "in_progress", "completed", "cancelled"] = "pending"


class JobResponse(BaseModel):
    id: uuid.UUID
    origin: uuid.UUID
    destiny: uuid.UUID
    car_id: uuid.UUID
    driver_id: uuid.UUID
    created_by: uuid.UUID
    m3: int
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class JobUpdate(BaseModel):
    driver_id: Optional[uuid.UUID] = None
    car_id: Optional[uuid.UUID] = None
    m3: Optional[int] = None
    status: Optional[Literal["pending", "in_progress", "completed", "cancelled"]] = None
