from typing import Optional
import uuid
from pydantic import BaseModel


class CarBase(BaseModel):
    model: str
    license: str
    driver_id: uuid.UUID
    manufacture: int | None = None
    km: int | None = None
    fuel: str | None = None
    strength: str | None = None
    capacity: str | None = None
    versatility: str | None = None
    active: bool
    image_url: str | None = None


class CarCreate(CarBase):
    pass

class UserNested(BaseModel):
    id: uuid.UUID
    name: str
    email: str

    class Config:
        from_attributes = True

class CarOut(CarBase):
    id: uuid.UUID
    driver: Optional[UserNested]

    class Config:
        from_attributes = True
