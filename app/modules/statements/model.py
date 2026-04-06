from datetime import datetime
from typing import TYPE_CHECKING
import uuid
from sqlmodel import Relationship, SQLModel, Field

if TYPE_CHECKING:
    from app.modules.jobs.model import Job


class Statement(SQLModel, table=True):
    __tablename__ = "statements"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

    job_id: uuid.UUID = Field(foreign_key="jobs.id", unique=True)

    status: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    job: "Job" = Relationship(back_populates="statement")
