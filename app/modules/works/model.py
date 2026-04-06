from typing import TYPE_CHECKING, List
import uuid
from sqlmodel import Relationship, SQLModel, Field
from sqlalchemy import text

if TYPE_CHECKING:
    from app.modules.jobs.model import Job


class Work(SQLModel, table=True):
    __tablename__ = "works"

    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        sa_column_kwargs={"server_default": text("gen_random_uuid()")},
    )
    name: str = Field(index=True)
    description: str | None = Field(default=None)
    address: str | None = Field(default=None)
    region: str | None = Field(default=None)
    city: str | None = Field(default=None)
    state: str | None = Field(default=None)
    budget: str | None = Field(default=None)
    status: str | None = Field(default="ativa")
    image_url: str | None = Field(default=None)

    # Relationship
    jobs_origin: List["Job"] = Relationship(
        back_populates="origin_work",
        sa_relationship_kwargs={"foreign_keys": "[Job.origin]"},
    )
    jobs_destiny: List["Job"] = Relationship(
        back_populates="destiny_work",
        sa_relationship_kwargs={"foreign_keys": "[Job.destiny]"},
    )
