from datetime import datetime, timezone
from typing import Optional
import uuid

from fastapi import HTTPException
from fastapi_async_sqlalchemy import db
from sqlalchemy import case, func, select
from sqlalchemy.orm import selectinload
from app.modules.jobs.model import Job, JobStatus
from app.modules.jobs.schema import JobCreate, JobUpdate, JobsCount
from app.modules.statements.model import Statement, StatementStatus
from app.modules.materials.model import Material
from app.modules.payments.model import Payment, PaymentStatus


async def list_jobs(offset: int = 0, limit: int = 20) -> list[Job]:
    result = await db.session.execute(
        select(Job)
        .options(
            selectinload(Job.origin_work),
            selectinload(Job.destiny_work),
            selectinload(Job.material),
            selectinload(Job.car),
            selectinload(Job.carrier),
            selectinload(Job.driver),
            selectinload(Job.creator),
            selectinload(Job.statement),
        )
        .offset(offset)
        .limit(limit)
        .order_by(Job.created_at.desc())
    )
    return result.scalars().all()


async def create_job(data: JobCreate, created_by: uuid.UUID) -> Job:
    # Se um statement foi informado, apenas validamos que ele existe
    # (statement não carrega mais material/m3 — isso já vem no próprio Job)
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
            raise HTTPException(status_code=404, detail="Manifesto não encontrado")

    material = (
        (
            await db.session.execute(
                select(Material).where(Material.id == data.material_id)
            )
        )
        .scalars()
        .first()
    )
    if not material:
        raise HTTPException(status_code=404, detail="Material não encontrado")

    job = Job(
        **data.model_dump(exclude_none=True),
        created_by=created_by,
        created_at=datetime.now(timezone.utc),
    )
    db.session.add(job)
    await db.session.flush()  # gera o job.id sem fechar a transação

    # 🔒 Payment só é lançado se o job já tiver um statement_id vinculado
    if job.statement_id:
        payment = Payment(
            job_id=job.id,
            total=job.value,
            status=PaymentStatus.PENDING,
        )
        db.session.add(payment)

    await db.session.commit()

    # 👇 recarrega já com todas as relações prontas, evitando lazy load depois
    return await get_job_by_id(job.id)


async def get_job_by_id(job_id: uuid.UUID) -> Job | None:
    result = await db.session.execute(
        select(Job)
        .where(Job.id == job_id)
        .options(
            selectinload(Job.origin_work),
            selectinload(Job.destiny_work),
            selectinload(Job.material),
            selectinload(Job.car),
            selectinload(Job.carrier),
            selectinload(Job.driver),
            selectinload(Job.creator),
            selectinload(Job.statement),
        )
    )
    return result.scalars().first()


async def update(job_id: uuid.UUID, data: JobUpdate) -> Job:
    job = await get_job_by_id(job_id)
    if not job:
        raise HTTPException(
            status_code=404, detail="Movimentação entre obras, não encontrada"
        )

    update_data = data.model_dump(exclude_unset=True)

    # 🔒 Uma vez vinculado, o statement_id não pode ser removido nem trocado
    if "statement_id" in update_data and job.statement_id is not None:
        if update_data["statement_id"] != job.statement_id:
            raise HTTPException(
                status_code=400,
                detail=(
                    "Não é possível alterar ou remover o manifesto (MTR) de um "
                    "job que já possui pagamento vinculado. Para desfazer, "
                    "cancele o job."
                ),
            )

    if "statement_id" in update_data and update_data["statement_id"]:
        statement = (
            (
                await db.session.execute(
                    select(Statement).where(Statement.id == update_data["statement_id"])
                )
            )
            .scalars()
            .first()
        )
        if not statement:
            raise HTTPException(status_code=404, detail="MTR não encontrado")

    if "material_id" in update_data and update_data["material_id"]:
        material = (
            (
                await db.session.execute(
                    select(Material).where(Material.id == update_data["material_id"])
                )
            )
            .scalars()
            .first()
        )
        if not material:
            raise HTTPException(status_code=404, detail="Material não encontrado")

    for field in update_data:
        setattr(job, field, getattr(data, field))

    existing_payment_result = await db.session.execute(
        select(Payment).where(Payment.job_id == job.id)
    )
    existing_payment = existing_payment_result.scalars().first()

    if job.status == JobStatus.CANCELED:
        # 🔁 Cancelamento em cascata: cancela o payment e o statement vinculados
        if existing_payment:
            existing_payment.status = PaymentStatus.CANCELED

        if job.statement_id:
            statement = (
                (
                    await db.session.execute(
                        select(Statement).where(Statement.id == job.statement_id)
                    )
                )
                .scalars()
                .first()
            )
            if statement:
                statement.status = StatementStatus.CANCELED
    else:
        # Fluxo normal: cria/atualiza o payment se houver statement_id
        if job.statement_id:
            if existing_payment:
                existing_payment.total = job.value
            else:
                db.session.add(
                    Payment(
                        job_id=job.id,
                        total=job.value,
                        status=PaymentStatus.PENDING,
                    )
                )

    await db.session.commit()
    await db.session.refresh(job)
    return job


async def delete(job_id: uuid.UUID) -> None:
    job = await get_job_by_id(job_id)
    if not job:
        raise HTTPException(
            status_code=404, detail="Movimentação entre obras, não encontrada"
        )

    # 🔒 Job com manifesto/pagamento vinculado não pode ser excluído
    if job.statement_id:
        raise HTTPException(
            status_code=400,
            detail=(
                "Não é possível excluir um job com manifesto (MTR) vinculado. "
                "Altere o status para 'cancelado' em vez de excluir."
            ),
        )

    await db.session.delete(job)
    await db.session.commit()


async def list_jobs_by_work_origin(work_id: uuid.UUID) -> list[Job]:
    result = await db.session.execute(
        select(Job)
        .where(Job.origin_id == work_id)
        .options(
            selectinload(Job.origin_work),
            selectinload(Job.destiny_work),
            selectinload(Job.material),
            selectinload(Job.car),
            selectinload(Job.carrier),
            selectinload(Job.driver),
            selectinload(Job.creator),
            selectinload(Job.statement),
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
            selectinload(Job.material),
            selectinload(Job.car),
            selectinload(Job.carrier),
            selectinload(Job.driver),
            selectinload(Job.creator),
            selectinload(Job.statement),
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
