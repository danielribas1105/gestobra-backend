from typing import Optional
import uuid
from pydantic import BaseModel, ConfigDict


class MaterialCreate(BaseModel):
    name: str
    description: Optional[str] = None
    value_m3: float


class MaterialUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    value_m3: Optional[float] = None


class MaterialResponse(BaseModel):
    id: uuid.UUID
    name: str
    description: Optional[str] = None
    value_m3: float

    model_config = ConfigDict(from_attributes=True)
