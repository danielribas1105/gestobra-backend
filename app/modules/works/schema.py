import uuid
from pydantic import BaseModel


class WorkBase(BaseModel):
    name: str
    description: str | None = None
    address: str | None = None
    region: str | None = None
    city: str | None = None
    state: str | None = None
    budget: str | None = None
    status: str | None = "ativa"
    image_url: str | None = None


class WorkCreate(WorkBase):
    pass


class WorkOut(WorkBase):
    id: uuid.UUID

    class Config:
        from_attributes = True
