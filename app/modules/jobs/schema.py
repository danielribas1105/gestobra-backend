import uuid
from pydantic import BaseModel

class JobBase(BaseModel):
    created_at: str
    updated_at: str
    origin: str
    destiny: str
    car_id: str
    user_id: str
    m3: int
    status: str

class JobCreate(JobBase):
    pass


class JobOut(JobBase):
    id: uuid.UUID

    class Config:
        from_attributes = True
