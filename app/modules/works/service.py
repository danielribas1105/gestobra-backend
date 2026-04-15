import uuid

from fastapi import HTTPException
from fastapi_async_sqlalchemy import db
from sqlalchemy import select
from app.modules.works.model import Work
from app.modules.works.schema import WorkCreate, WorkUpdate


async def list_works(offset: int = 0, limit: int = 20) -> list[Work]:
    result = await db.session.execute(select(Work).offset(offset).limit(limit))
    return result.scalars().all()


async def create_work(data: WorkCreate) -> Work:
    work = Work(**data.model_dump())
    db.session.add(work)
    await db.session.commit()
    await db.session.refresh(work)
    return work


async def get_work_by_id(work_id: uuid.UUID) -> Work | None:
    result = await db.session.execute(select(Work).where(Work.id == work_id))
    work = result.scalars().first()

    return work


async def update(work_id: str, data: WorkUpdate) -> Work:
    work = await get_work_by_id(work_id)
    if not work:
        raise HTTPException(status_code=404, detail="Obra não encontrada")
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(work, field, value)
    await db.session.commit()
    await db.session.refresh(work)
    return work


async def delete(work_id: str) -> None:
    work = await get_work_by_id(work_id)
    if not work:
        raise HTTPException(status_code=404, detail="Obra não encontrada")
    await db.session.delete(work)
    await db.session.commit()
