from datetime import datetime
from typing import TYPE_CHECKING, Optional
import uuid
from sqlalchemy import Column, DateTime, func
from sqlmodel import Relationship, SQLModel, Field

if TYPE_CHECKING:
    from app.modules.jobs.model import Job


class Statement(SQLModel, table=True):
    __tablename__ = "statements"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

    job_id: uuid.UUID = Field(foreign_key="jobs.id", unique=True)

    status: str
    created_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), server_default=func.now()),
    )

    job: "Job" = Relationship(back_populates="statement")
