from datetime import datetime
import enum
from typing import TYPE_CHECKING, List, Optional
import uuid
from sqlmodel import Relationship, SQLModel, Field
from sqlalchemy import Column, DateTime, String, func, text

if TYPE_CHECKING:
    from app.modules.jobs.model import Job


class WorkStatus(str, enum.Enum):
    ATIVA = "active"
    INATIVA = "inactive"
    PARALIZADA = "paralyzed"
    BLOQUEADA = "blocked"
    FINALIZADA = "finished"


class Work(SQLModel, table=True):
    __tablename__ = "works"

    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        sa_column_kwargs={"server_default": text("gen_random_uuid()")},
    )
    code: str = Field(index=True)
    name: str = Field(index=True)
    cnpj: Optional[str] = Field(default=None, nullable=True)
    description: Optional[str] = Field(default=None, nullable=True)
    address: Optional[str] = Field(default=None, nullable=True)
    zip_code: Optional[str] = Field(default=None, nullable=True)
    city: Optional[str] = Field(default=None, nullable=True)
    state: Optional[str] = Field(default=None, nullable=True)
    status: WorkStatus = Field(
        default=WorkStatus.ATIVA,
        sa_column=Column(
            String(50),
            nullable=False,
            server_default=WorkStatus.ATIVA.value,
        ),
    )
    created_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), server_default=func.now()),
    )

    # Relationship
    jobs_origin: List["Job"] = Relationship(
        back_populates="origin_work",
        sa_relationship_kwargs={"foreign_keys": "[Job.origin]"},
    )
    jobs_destiny: List["Job"] = Relationship(
        back_populates="destiny_work",
        sa_relationship_kwargs={"foreign_keys": "[Job.destiny]"},
    )
