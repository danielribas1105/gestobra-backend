from typing import Optional
import uuid
from pydantic import BaseModel, ConfigDict


# Data to create a car (input)
class CarCreate(BaseModel):
    model: str
    license: str
    manufacture: int | None = None
    km: int | None = None
    fuel: str | None = None
    strength: str | None = None
    capacity: str | None = None
    versatility: str | None = None
    active: bool = True
    image: str | None = None


class CarUpdate(BaseModel):
    model: Optional[str] = None
    license: Optional[str] = None
    manufacture: Optional[int] = None
    km: Optional[int] = None
    fuel: Optional[str] = None
    strength: Optional[str] = None
    capacity: Optional[str] = None
    versatility: Optional[str] = None
    active: Optional[bool] = None
    image: Optional[str] = None


# Data returned to the client (output — never exposes the password)
class CarResponse(BaseModel):
    id: uuid.UUID
    model: str
    license: str
    manufacture: int | None = None
    km: int | None = None
    fuel: str | None = None
    strength: str | None = None
    capacity: str | None = None
    versatility: str | None = None
    active: bool
    image: str | None = None

    model_config = ConfigDict(from_attributes=True)
