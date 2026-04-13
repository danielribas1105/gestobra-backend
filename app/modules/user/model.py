import uuid
from datetime import datetime
from typing import TYPE_CHECKING, List, Optional
from sqlalchemy import Column, DateTime, func
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.modules.car.model import Car
    from app.modules.jobs.model import Job


class User(SQLModel, table=True):
    __tablename__ = "users"  # type: ignore

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str
    email: str = Field(unique=True, index=True)
    password_hash: Optional[str] = Field(default=None, nullable=True)
    email_verified: bool = Field(default=False)
    image: Optional[str] = Field(default=None, nullable=True)
    profile: str = Field(default="operator")
    active: bool = Field(default=True)
    created_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), server_default=func.now()),
    )
    updated_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), onupdate=func.now()),
    )

    # Relationship
    created_jobs: List["Job"] = Relationship(
        back_populates="creator",
        sa_relationship_kwargs={"foreign_keys": "[Job.created_by]"},
    )
    driven_jobs: List["Job"] = Relationship(
        back_populates="driver",
        sa_relationship_kwargs={"foreign_keys": "[Job.driver_id]"},
    )
