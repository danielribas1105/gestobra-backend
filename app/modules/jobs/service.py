from datetime import datetime, timezone
from typing import Optional
import uuid

from fastapi import HTTPException
from fastapi_async_sqlalchemy import db
from sqlalchemy import case, func, select
from sqlalchemy.orm import selectinload
from app.modules.jobs.model import Job, JobStatus
from app.modules.jobs.schema import JobCreate, JobUpdate, JobsCount
from app.modules.statements.model import Statement
from app.modules.materials.model import Material
from app.modules.payments.model import Payment, PaymentStatus


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
    job = Job(
        **data.model_dump(exclude_none=True),
        created_by=created_by,
        created_at=datetime.now(timezone.utc),
    )
    db.session.add(job)
    await db.session.flush()  # gera o job.id sem fechar a transação

    if data.statement_id:
        statement = (
            (
                await db.session.execute(
                    select(Statement).where(Statement.id == data.statement_id)
                )
            )
            .scalars()
            .first()
        )

        if not statement:
            raise HTTPException(status_code=404, detail="Medição não encontrada")

        material = (
            (
                await db.session.execute(
                    select(Material).where(Material.id == statement.material_id)
                )
            )
            .scalars()
            .first()
        )

        if not material:
            raise HTTPException(status_code=404, detail="Material não encontrado")

        payment = Payment(
            job_id=job.id,
            m3=statement.m3,
            value_m3=material.value_m3,
            total=statement.m3 * material.value_m3,
            status=PaymentStatus.PENDING,
        )
        db.session.add(payment)

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

    old_statement_id = job.statement_id

    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(job, field, value)

    new_statement_id = (
        data.statement_id if "statement_id" in data.model_fields_set else None
    )

    if new_statement_id and new_statement_id != old_statement_id:
        statement = (
            (
                await db.session.execute(
                    select(Statement).where(Statement.id == new_statement_id)
                )
            )
            .scalars()
            .first()
        )

        if not statement:
            raise HTTPException(status_code=404, detail="MTR não encontrado")

        material = (
            (
                await db.session.execute(
                    select(Material).where(Material.id == statement.material_id)
                )
            )
            .scalars()
            .first()
        )

        if not material:
            raise HTTPException(status_code=404, detail="Material não encontrado")

        # Busca payment existente para este job
        existing_payment_result = await db.session.execute(
            select(Payment).where(Payment.job_id == job.id)
        )
        existing_payment = existing_payment_result.scalars().first()

        if existing_payment:
            # Atualiza o payment existente
            existing_payment.m3 = statement.m3
            existing_payment.value_m3 = material.value_m3
            existing_payment.total = statement.m3 * material.value_m3
        else:
            # Cria um novo payment
            new_payment = Payment(
                job_id=job.id,
                m3=statement.m3,
                value_m3=material.value_m3,
                total=statement.m3 * material.value_m3,
                status=PaymentStatus.PENDING,
            )
            db.session.add(new_payment)

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


async def count_jobs() -> JobsCount:
    result = await db.session.execute(
        select(
            func.coalesce(
                func.sum(
                    case(
                        (Job.status == JobStatus.CONCLUDED, 1),
                        else_=0,
                    )
                ),
                0,
            ).label("concluded"),
            func.coalesce(
                func.sum(
                    case(
                        (Job.status == JobStatus.IN_PROGRESS, 1),
                        else_=0,
                    )
                ),
                0,
            ).label("in_progress"),
            func.coalesce(
                func.sum(
                    case(
                        (Job.status == JobStatus.PENDING, 1),
                        else_=0,
                    )
                ),
                0,
            ).label("pending"),
            func.coalesce(
                func.sum(
                    case(
                        (Job.status == JobStatus.CANCELED, 1),
                        else_=0,
                    )
                ),
                0,
            ).label("canceled"),
        ).select_from(Job)
    )

    row = result.mappings().one()

    return JobsCount(
        concluded=row["concluded"],
        in_progress=row["in_progress"],
        pending=row["pending"],
        canceled=row["canceled"],
    )
