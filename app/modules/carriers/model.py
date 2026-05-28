from datetime import datetime
from typing import TYPE_CHECKING, List, Optional
import uuid
from sqlmodel import Relationship, SQLModel, Field
from sqlalchemy import Column, DateTime, String, func, text

if TYPE_CHECKING:
    from app.modules.jobs.model import Job


class Carrier(SQLModel, table=True):
    __tablename__ = "carriers"

    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        sa_column_kwargs={"server_default": text("gen_random_uuid()")},
    )
    code: str = Field(index=True)
    name: str = Field(index=True)
    cnpj: Optional[str] = Field(default=None, nullable=True)
    phone: Optional[str] = Field(default=None, nullable=True)
    address: Optional[str] = Field(default=None, nullable=True)
    zip_code: Optional[str] = Field(default=None, nullable=True)
    city: Optional[str] = Field(default=None, nullable=True)
    state: Optional[str] = Field(default=None, nullable=True)
    created_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), server_default=func.now()),
    )

    # Relationship
    jobs: List["Job"] = Relationship(back_populates="carriers")
