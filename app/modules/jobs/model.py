from datetime import datetime
from typing import TYPE_CHECKING, Optional
import uuid
from sqlmodel import Relationship, SQLModel, Field
from sqlalchemy import text

if TYPE_CHECKING:
    from app.modules.user.model import User
    from app.modules.car.model import Car
    from app.modules.works.model import Work
    from app.modules.statements.model import Statement


class Job(SQLModel, table=True):
    __tablename__ = "jobs"

    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        sa_column_kwargs={"server_default": text("gen_random_uuid()")},
    )
    origin: uuid.UUID = Field(foreign_key="works.id", nullable=False, index=True)
    destiny: uuid.UUID = Field(foreign_key="works.id", nullable=False, index=True)
    car_id: uuid.UUID = Field(foreign_key="cars.id", nullable=False, index=True)
    created_by: uuid.UUID = Field(foreign_key="users.id", nullable=False, index=True)
    m3: int = Field()
    status: str = Field()
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    # Relationship
    car: Optional["Car"] = Relationship(back_populates="jobs")
    statement: Optional["Statement"] = Relationship(back_populates="job")
    creator: Optional["User"] = Relationship(
        back_populates="created_jobs",
        sa_relationship_kwargs={"foreign_keys": "[Job.created_by]"},
    )
    origin_work: Optional["Work"] = Relationship(
        back_populates="jobs_origin",
        sa_relationship_kwargs={"foreign_keys": "[Job.origin]"},
    )
    destiny_work: Optional["Work"] = Relationship(
        back_populates="jobs_destiny",
        sa_relationship_kwargs={"foreign_keys": "[Job.destiny]"},
    )
