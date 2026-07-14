from datetime import datetime
import enum
from typing import TYPE_CHECKING, Optional
import uuid
from sqlmodel import Relationship, SQLModel, Field
from sqlalchemy import Column, DateTime, String, func, text

if TYPE_CHECKING:
    from app.modules.user.model import User
    from app.modules.car.model import Car
    from app.modules.carriers.model import Carrier
    from app.modules.works.model import Work
    from app.modules.statements.model import Statement
    from app.modules.payments.model import Payment
    from app.modules.materials.model import Material


class JobStatus(str, enum.Enum):
    CONCLUDED = "concluded"
    IN_PROGRESS = "in_progress"
    PENDING = "pending"
    CANCELED = "canceled"


class ValueType(str, enum.Enum):
    PER_QUANTITY = "per_quantity"
    PER_TRIP = "per_trip"
    PER_KM = "per_km"


class Job(SQLModel, table=True):
    __tablename__ = "jobs"

    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        sa_column_kwargs={"server_default": text("gen_random_uuid()")},
    )
    statement_id: uuid.UUID = Field(
        unique=True,
        default=None,
        foreign_key="statements.id",
        nullable=True,
    )
    origin_id: uuid.UUID = Field(foreign_key="works.id", nullable=False, index=True)
    destiny_id: uuid.UUID = Field(foreign_key="works.id", nullable=False, index=True)
    material_id: uuid.UUID = Field(
        foreign_key="materials.id", nullable=False, index=True
    )
    quantity: float = Field()
    unit: Optional[str] = Field(default=None)
    value_type: ValueType = Field(
        default=ValueType.PER_QUANTITY,
        sa_column=Column(
            String(50),
            nullable=False,
            default=ValueType.PER_QUANTITY.value,
            server_default=ValueType.PER_QUANTITY.value,
        ),
    )
    rate: float = Field(
        nullable=False
    )  # o valor unitário negociado por quantidade ou viagem
    value: float = Field(nullable=False)
    car_id: uuid.UUID = Field(foreign_key="cars.id", nullable=False, index=True)
    carrier_id: uuid.UUID = Field(foreign_key="carriers.id", nullable=False, index=True)
    created_by: uuid.UUID = Field(foreign_key="users.id", nullable=False, index=True)
    driver_id: uuid.UUID = Field(foreign_key="users.id", nullable=False, index=True)
    status: JobStatus = Field(
        default=JobStatus.PENDING,
        sa_column=Column(
            String(50),
            nullable=False,
            default=JobStatus.PENDING.value,
            server_default=JobStatus.PENDING.value,
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

    # Relationship
    material: Optional["Material"] = Relationship(back_populates="jobs")
    car: Optional["Car"] = Relationship(back_populates="jobs")
    carrier: Optional["Carrier"] = Relationship(back_populates="jobs")
    statement: Optional["Statement"] = Relationship(back_populates="job")
    payment: Optional["Payment"] = Relationship(back_populates="job")
    creator: Optional["User"] = Relationship(
        back_populates="created_jobs",
        sa_relationship_kwargs={"foreign_keys": "[Job.created_by]"},
    )
    driver: Optional["User"] = Relationship(
        back_populates="driven_jobs",
        sa_relationship_kwargs={"foreign_keys": "[Job.driver_id]"},
    )
    origin_work: Optional["Work"] = Relationship(
        back_populates="jobs_origin",
        sa_relationship_kwargs={"foreign_keys": "[Job.origin_id]"},
    )
    destiny_work: Optional["Work"] = Relationship(
        back_populates="jobs_destiny",
        sa_relationship_kwargs={"foreign_keys": "[Job.destiny_id]"},
    )
