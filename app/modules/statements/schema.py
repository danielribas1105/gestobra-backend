from typing import List
import uuid
from pydantic import BaseModel


class StatementBase(BaseModel):
    name: str
    created_at: str
    active: bool

class StatementCreate(StatementBase):
    pass

class StatementOut(StatementBase):
    id: uuid.UUID

    class Config:
        from_attributes = True
