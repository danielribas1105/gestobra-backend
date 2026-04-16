from typing import TYPE_CHECKING, List, Optional
import uuid
from sqlalchemy import text
from sqlmodel import Relationship, SQLModel, Field

from app.modules.statements.model import Statement

if TYPE_CHECKING:
    from app.modules.statements.model import Statement


class Material(SQLModel, table=True):
    __tablename__ = "materials"

    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        sa_column_kwargs={"server_default": text("gen_random_uuid()")},
    )
    name: str = Field(nullable=False)
    description: Optional[str] = Field(default=None)
    value_m3: float = Field(nullable=False)

    # Relationship
    # A material can appear in multiple statements
    statements: List["Statement"] = Relationship(back_populates="material")
