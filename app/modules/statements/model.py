from datetime import datetime
import enum
from typing import TYPE_CHECKING, Optional
import uuid
from sqlalchemy import Column, DateTime, String, func, text
from sqlmodel import Relationship, SQLModel, Field

if TYPE_CHECKING:
    from app.modules.jobs.model import Job
    from app.modules.materials.model import Material


class StatementStatus(str, enum.Enum):
    APPROVED = "approved"
    PENDING = "pending"
    REJECTED = "rejected"
    CONCLUDED = "concluded"


class Statement(SQLModel, table=True):
    __tablename__ = "statements"

    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        sa_column_kwargs={"server_default": text("gen_random_uuid()")},
    )
    code: Optional[str] = Field(default=None)
    material_id: uuid.UUID = Field(
        foreign_key="materials.id", nullable=False, index=True
    )
    m3: int = Field()
    active: bool = Field(default=True, sa_column_kwargs={"server_default": "true"})
    status: StatementStatus = Field(
        default=StatementStatus.PENDING,
        sa_column=Column(
            String(50),
            nullable=False,
            server_default=StatementStatus.PENDING.value,
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

    job: Optional["Job"] = Relationship(back_populates="statement")
    material: "Material" = Relationship(back_populates="statements")
