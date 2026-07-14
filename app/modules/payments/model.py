from datetime import datetime
from typing import TYPE_CHECKING, Optional
import uuid
from sqlalchemy import Column, DateTime, String, func, text
from sqlmodel import Relationship, SQLModel, Field
import enum

if TYPE_CHECKING:
    from app.modules.jobs.model import Job


class PaymentStatus(str, enum.Enum):
    PENDING = "pending"
    PAID = "paid"
    CANCELED = "canceled"


class Payment(SQLModel, table=True):
    __tablename__ = "payments"

    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        sa_column_kwargs={"server_default": text("gen_random_uuid()")},
    )
    job_id: uuid.UUID = Field(
        foreign_key="jobs.id", unique=True, nullable=False, index=True
    )
    total: float = Field(
        nullable=False
    )  # snapshot de job.value no momento do lançamento
    status: PaymentStatus = Field(
        default=PaymentStatus.PENDING,
        sa_column=Column(
            String(50),
            nullable=False,
            server_default=PaymentStatus.PENDING.value,
        ),
    )
    created_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), server_default=func.now()),
    )
    updated_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), onupdate=func.now()),
    )

    job: Optional["Job"] = Relationship(back_populates="payment")
