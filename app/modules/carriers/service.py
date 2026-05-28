import uuid

from fastapi import HTTPException
from fastapi_async_sqlalchemy import db
from sqlalchemy import select
from app.modules.carriers.model import Carrier
from app.modules.works.schema import WorkCreate, WorkUpdate


async def list_carriers(offset: int = 0, limit: int = 20) -> list[Carrier]:
    result = await db.session.execute(select(Carrier).offset(offset).limit(limit))
    return result.scalars().all()
