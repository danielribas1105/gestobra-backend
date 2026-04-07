from datetime import datetime
import uuid
from pydantic import BaseModel, ConfigDict


class JobCreate(BaseModel):
    origin: uuid.UUID
    destiny: uuid.UUID
    car_id: uuid.UUID
    created_by: uuid.UUID
    m3: int
    status: str


class JobResponse(BaseModel):
    id: uuid.UUID
    origin: uuid.UUID
    destiny: uuid.UUID
    car_id: uuid.UUID
    created_by: uuid.UUID
    m3: int
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
