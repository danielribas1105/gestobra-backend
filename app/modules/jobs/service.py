from datetime import datetime, timezone
from typing import Optional
import uuid

from fastapi import HTTPException
from fastapi_async_sqlalchemy import db
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.modules.jobs.model import Job
from app.modules.jobs.schema import JobCreate, JobUpdate
from app.modules.statements.model import Statement


async def list_jobs(offset: int = 0, limit: int = 20) -> list[Job]:
    result = await db.session.execute(
        select(Job)
        .options(
            selectinload(Job.origin_work),
            selectinload(Job.destiny_work),
            selectinload(Job.car),
            selectinload(Job.driver),
            selectinload(Job.creator),
            selectinload(Job.statement),
            selectinload(Job.statement).selectinload(Statement.material),
        )
        .offset(offset)
        .limit(limit)
    )
    return result.scalars().all()


async def create_job(data: JobCreate, created_by: uuid.UUID) -> Job:
    print(f"job {data}")
    job = Job(
        **data.model_dump(exclude_none=True),
        created_by=created_by,
        created_at=datetime.now(timezone.utc),
    )
    db.session.add(job)
    await db.session.commit()
    await db.session.refresh(job)
    return job


async def get_job_by_id(job_id: uuid.UUID) -> Job | None:
    result = await db.session.execute(select(Job).where(Job.id == job_id))
    job = result.scalars().first()

    return job


async def update(job_id: uuid.UUID, data: JobUpdate) -> Job:
    job = await get_job_by_id(job_id)
    if not job:
        raise HTTPException(
            status_code=404, detail="Movimentação entre obras, não encontrada"
        )
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(job, field, value)
    await db.session.commit()
    await db.session.refresh(job)
    return job


async def delete(job_id: uuid.UUID) -> None:
    job = await get_job_by_id(job_id)
    if not job:
        raise HTTPException(
            status_code=404, detail="Movimentação entre obras, não encontrada"
        )
    await db.session.delete(job)
    await db.session.commit()


async def list_jobs_by_work_origin(work_id: uuid.UUID) -> list[Job]:
    result = await db.session.execute(
        select(Job)
        .where(Job.origin == work_id)
        .options(
            selectinload(Job.origin_work),
            selectinload(Job.destiny_work),
            selectinload(Job.car),
            selectinload(Job.driver),
            selectinload(Job.creator),
            selectinload(Job.statement),
            selectinload(Job.statement).selectinload(Statement.material),
        )
    )
    return result.scalars().all()


async def get_job_by_statement_id(statement_id: uuid.UUID) -> Optional[Job]:
    result = await db.session.execute(
        select(Job)
        .where(Job.statement_id == statement_id)
        .options(
            selectinload(Job.origin_work),
            selectinload(Job.destiny_work),
            selectinload(Job.car),
            selectinload(Job.driver),
            selectinload(Job.creator),
            selectinload(Job.statement).selectinload(Statement.material),
        )
    )
    return result.scalars().first()
