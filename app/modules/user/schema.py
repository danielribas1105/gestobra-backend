import uuid

from pydantic import BaseModel, ConfigDict, EmailStr
from datetime import datetime
from typing import Optional


# Data to create a user (input)
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    email_verified: Optional[bool] = False
    image: Optional[str] = None
    profile: Optional[str] = "user"
    active: bool
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


# Data returned to the client (output — never exposes the password)
class UserResponse(BaseModel):
    id: uuid.UUID
    name: str
    email: str
    email_verified: bool | None = None
    image: str | None = None
    profile: str | None = None
    active: bool
    created_at: datetime | None = None
    updated_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


class UserUpdate(BaseModel):
    name: Optional[str] = None
    image: Optional[str] = None
    profile: Optional[str] = None
    active: Optional[bool] = None


# Login schema
class LoginRequest(BaseModel):
    email: EmailStr
    password: str
