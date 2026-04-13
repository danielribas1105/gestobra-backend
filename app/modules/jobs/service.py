import uuid

from fastapi_async_sqlalchemy import db
from sqlalchemy import select
from app.modules.jobs.model import Job
from app.modules.jobs.schema import JobCreate


async def list_jobs(offset: int = 0, limit: int = 20) -> list[Job]:
    result = await db.session.execute(select(Job).offset(offset).limit(limit))
    return result.scalars().all()


async def create_job(data: JobCreate, created_by: uuid.UUID) -> Job:
    job = Job(**data.model_dump(), created_by=created_by)
    db.session.add(job)
    await db.session.commit()
    await db.session.refresh(job)
    return job


async def get_job_by_id(job_id: uuid.UUID) -> Job | None:
    result = await db.session.execute(select(Job).where(Job.id == job_id))
    job = result.scalars().first()

    return job
