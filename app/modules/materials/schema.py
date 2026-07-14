from typing import Optional
import uuid
from pydantic import BaseModel, ConfigDict


class MaterialCreate(BaseModel):
    code: Optional[str] = None
    name: str
    state: Optional[str] = None
    material_class: Optional[str] = None
    packaging: Optional[str] = None
    technology: Optional[str] = None


class MaterialUpdate(BaseModel):
    code: Optional[str] = None
    name: Optional[str] = None
    state: Optional[str] = None
    material_class: Optional[str] = None
    packaging: Optional[str] = None
    technology: Optional[str] = None


class MaterialResponse(BaseModel):
    id: uuid.UUID
    code: Optional[str] = None
    name: str
    state: Optional[str] = None
    material_class: Optional[str] = None
    packaging: Optional[str] = None
    technology: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
