from datetime import datetime
import uuid
from pydantic import BaseModel, ConfigDict
from app.modules.payments.model import PaymentStatus


class PaymentResponse(BaseModel):
    id: uuid.UUID
    job_id: uuid.UUID
    m3: int
    value_m3: float
    total: float
    status: PaymentStatus
    created_at: datetime | None = None
    updated_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


class PaymentUpdate(BaseModel):
    m3: int | None = None
    value_m3: float | None = None
    status: PaymentStatus | None = None


class PaymentBatchUpdateItem(BaseModel):
    id: uuid.UUID
    status: PaymentStatus
    updated_at: datetime | None = None


class PaymentBatchUpdate(BaseModel):
    updates: list[PaymentBatchUpdateItem]


class PaymentsTotalValues(BaseModel):
    paid: float
    pending: float
    canceled: float


class CarPaymentSummary(BaseModel):
    license: str
    model: str
    pending: float
    paid: float
    canceled: float
    total: float
