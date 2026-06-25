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


class JobStatus(str, enum.Enum):
    CONCLUDED = "concluded"
    IN_PROGRESS = "in_progress"
    PENDING = "pending"
    CANCELED = "canceled"


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
    origin: uuid.UUID = Field(foreign_key="works.id", nullable=False, index=True)
    destiny: uuid.UUID = Field(foreign_key="works.id", nullable=False, index=True)
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
        sa_relationship_kwargs={"foreign_keys": "[Job.origin]"},
    )
    destiny_work: Optional["Work"] = Relationship(
        back_populates="jobs_destiny",
        sa_relationship_kwargs={"foreign_keys": "[Job.destiny]"},
    )
