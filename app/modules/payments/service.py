import uuid
from fastapi import HTTPException
from fastapi_async_sqlalchemy import db
from sqlmodel import select
from sqlalchemy import func, case
from app.modules.car.model import Car
from app.modules.payments.model import Payment, PaymentStatus
from app.modules.payments.schema import (
    CarPaymentSummary,
    PaymentUpdate,
    PaymentsTotalValues,
)
from app.modules.jobs.model import Job, JobStatus
from app.modules.statements.model import Statement
from app.modules.materials.model import Material


async def list_payments(offset: int = 0, limit: int = 20) -> list[Payment]:
    result = await db.session.execute(select(Payment).offset(offset).limit(limit))
    return result.scalars().all()


async def get_payment_by_id(payment_id: uuid.UUID) -> Payment | None:
    result = await db.session.execute(select(Payment).where(Payment.id == payment_id))
    return result.scalars().first()


async def update(payment_id: uuid.UUID, data: PaymentUpdate) -> Payment:
    payment = await get_payment_by_id(payment_id)
    if not payment:
        raise HTTPException(status_code=404, detail="Pagamento não encontrado")

    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(payment, field, value)
    await db.session.commit()
    await db.session.refresh(payment)
    return payment


async def payments_total_values() -> PaymentsTotalValues:
    result = await db.session.execute(
        select(
            func.coalesce(
                func.sum(
                    case(
                        (Payment.status == PaymentStatus.PAID, Payment.total),
                        else_=0,
                    )
                ),
                0,
            ).label("paid"),
            func.coalesce(
                func.sum(
                    case(
                        (Payment.status == PaymentStatus.PENDING, Payment.total),
                        else_=0,
                    )
                ),
                0,
            ).label("pending"),
            func.coalesce(
                func.sum(
                    case(
                        (Payment.status == PaymentStatus.CANCELED, Payment.total),
                        else_=0,
                    )
                ),
                0,
            ).label("canceled"),
        )
    )

    row = result.mappings().one()

    return PaymentsTotalValues(
        paid=row["paid"],
        pending=row["pending"],
        canceled=row["canceled"],
    )


async def generate_payment(job_id: uuid.UUID) -> Payment:
    # Carrega o job com statement e material
    job = (
        (await db.session.execute(select(Job).where(Job.id == job_id)))
        .scalars()
        .first()
    )

    if not job:
        raise HTTPException(status_code=404, detail="Job não encontrado")

    if job.status != JobStatus.COMPLETED:
        raise HTTPException(status_code=400, detail="Job ainda não concluído")

    statement = (
        (
            await db.session.execute(
                select(Statement).where(Statement.id == job.statement_id)
            )
        )
        .scalars()
        .first()
    )

    material = (
        (
            await db.session.execute(
                select(Material).where(Material.id == statement.material_id)
            )
        )
        .scalars()
        .first()
    )

    total = statement.m3 * material.value_m3

    payment = Payment(
        job_id=job_id,
        m3=statement.m3,
        value_m3=material.value_m3,
        total=total,
        status=PaymentStatus.PENDING,
    )
    db.session.add(payment)
    await db.session.commit()
    await db.session.refresh(payment)
    return payment


async def get_payment_by_job(job_id: uuid.UUID) -> Payment | None:
    result = await db.session.execute(select(Payment).where(Payment.job_id == job_id))
    return result.scalars().first()


async def get_sum_payments_by_car() -> list[CarPaymentSummary]:
    result = await db.session.execute(
        select(
            Car.license,
            Car.model,
            func.coalesce(
                func.sum(
                    case(
                        (Payment.status == PaymentStatus.PENDING, Payment.total),
                        else_=0,
                    )
                ),
                0,
            ).label("pending"),
            func.coalesce(
                func.sum(
                    case((Payment.status == PaymentStatus.PAID, Payment.total), else_=0)
                ),
                0,
            ).label("paid"),
            func.coalesce(
                func.sum(
                    case(
                        (Payment.status == PaymentStatus.CANCELED, Payment.total),
                        else_=0,
                    )
                ),
                0,
            ).label("canceled"),
            func.coalesce(func.sum(Payment.total), 0).label("total"),
        )
        .join(Job, Job.car_id == Car.id)
        .join(Payment, Payment.job_id == Job.id)
        .group_by(Car.license, Car.model)
        .order_by(Car.license)
    )

    rows = result.mappings().all()
    return [
        CarPaymentSummary(
            license=row["license"],
            model=row["model"],
            pending=row["pending"],
            paid=row["paid"],
            canceled=row["canceled"],
            total=row["total"],
        )
        for row in rows
    ]


async def get_payments_by_license(license: str) -> list[Payment]:
    result = await db.session.execute(
        select(Payment)
        .join(Job, Job.id == Payment.job_id)
        .join(Car, Car.id == Job.car_id)
        .where(Car.license == license)
        .order_by(Payment.created_at.desc())
    )
    return result.scalars().all()
