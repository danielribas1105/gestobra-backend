from typing import TYPE_CHECKING, List, Optional
import uuid
from sqlalchemy import text
from sqlmodel import Relationship, SQLModel, Field

if TYPE_CHECKING:
    from app.modules.jobs.model import Job


class Material(SQLModel, table=True):
    __tablename__ = "materials"

    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        sa_column_kwargs={"server_default": text("gen_random_uuid()")},
    )
    code: Optional[str] = Field(default=None)
    name: str = Field(nullable=False)
    state: Optional[str] = Field(default=None)
    material_class: Optional[str] = Field(default=None)
    packaging: Optional[str] = Field(default=None)
    technology: Optional[str] = Field(default=None)

    # Relationship
    # A material can appear in multiple jobs
    jobs: List["Job"] = Relationship(back_populates="material")
