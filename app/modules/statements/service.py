from datetime import datetime, timezone
from typing import Optional
import uuid
from fastapi import HTTPException
from fastapi_async_sqlalchemy import db
from sqlalchemy import case, func
from sqlmodel import select
from app.modules.jobs.model import Job
from app.modules.statements.model import Statement, StatementStatus
from app.modules.statements.schema import (
    StatementCreate,
    StatementUpdate,
    StatementsCount,
)


async def list_statements(offset: int = 0, limit: int = 20) -> list[Statement]:
    result = await db.session.execute(select(Statement).offset(offset).limit(limit))
    return result.scalars().all()


async def list_statements_without_job(
    offset: int = 0, limit: int = 20
) -> list[Statement]:
    result = await db.session.execute(
        select(Statement)
        .outerjoin(Job, Job.statement_id == Statement.id)
        .where(Job.id.is_(None))
        .offset(offset)
        .limit(limit)
    )
    return result.scalars().all()


async def create_statement(data: StatementCreate) -> Statement:
    statement = Statement(
        **data.model_dump(exclude_none=True),
        created_at=datetime.now(timezone.utc),
    )
    db.session.add(statement)
    await db.session.commit()
    await db.session.refresh(statement)
    return statement


async def get_statement_by_id(statement_id: uuid.UUID) -> Statement:
    result = await db.session.execute(
        select(Statement).where(Statement.id == statement_id)
    )
    statement = result.scalars().first()

    return statement


async def update(statement_id: uuid.UUID, data: StatementUpdate) -> Statement:
    statement = await get_statement_by_id(statement_id)
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(statement, field, value)
    statement.updated_at = datetime.now(timezone.utc)
    await db.session.commit()
    await db.session.refresh(statement)
    return statement


async def delete(statement_id: uuid.UUID) -> None:
    statement = await get_statement_by_id(statement_id)
    if not statement:
        raise HTTPException(status_code=404, detail="Manifesto não encontrado")

    job_result = await db.session.execute(
        select(Job).where(Job.statement_id == statement_id)
    )
    if job_result.scalars().first():
        raise HTTPException(
            status_code=400,
            detail=(
                "Não é possível excluir um manifesto vinculado a um job. "
                "Cancele o job para desfazer o vínculo."
            ),
        )

    await db.session.delete(statement)
    await db.session.commit()


async def get_statement_by_job_id(job_id: uuid.UUID) -> Optional[Statement]:
    result = await db.session.execute(
        select(Statement)
        .join(Job, Job.statement_id == Statement.id)
        .where(Job.id == job_id)
    )
    return result.scalars().first()


async def count_statements() -> StatementsCount:
    result = await db.session.execute(
        select(
            func.coalesce(
                func.sum(
                    case(
                        (Statement.status == StatementStatus.CONCLUDED, 1),
                        else_=0,
                    )
                ),
                0,
            ).label("concluded"),
            func.coalesce(
                func.sum(
                    case(
                        (Statement.status == StatementStatus.IN_PROGRESS, 1),
                        else_=0,
                    )
                ),
                0,
            ).label("in_progress"),
            func.coalesce(
                func.sum(
                    case(
                        (Statement.status == StatementStatus.PENDING, 1),
                        else_=0,
                    )
                ),
                0,
            ).label("pending"),
            func.coalesce(
                func.sum(
                    case(
                        (Statement.status == StatementStatus.CANCELED, 1),
                        else_=0,
                    )
                ),
                0,
            ).label("canceled"),
        ).select_from(Statement)
    )

    row = result.mappings().one()

    return StatementsCount(
        concluded=row["concluded"],
        in_progress=row["in_progress"],
        pending=row["pending"],
        canceled=row["canceled"],
    )
