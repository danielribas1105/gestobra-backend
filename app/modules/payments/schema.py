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
    status: PaymentStatus | None = None


class PaymentsTotalValues(BaseModel):
    paid: float
    pending: float
    canceled: float
