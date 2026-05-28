from datetime import datetime
from typing import Optional
import uuid
from pydantic import BaseModel, ConfigDict


class CarrierCreate(BaseModel):
    code: str
    name: str
    cnpj: str | None = None
    phone: str | None = None
    address: str | None = None
    zip_code: str | None = None
    city: str | None = None
    state: str | None = None


class CarrierUpdate(BaseModel):
    code: Optional[str] = None
    name: Optional[str] = None
    cnpj: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    zip_code: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None


class CarrierResponse(BaseModel):
    id: uuid.UUID
    code: str
    name: str
    cnpj: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    zip_code: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    created_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)
