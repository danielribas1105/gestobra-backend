import uuid
from fastapi_async_sqlalchemy import db
from sqlmodel import select
from app.modules.statements.model import Statement
from app.modules.statements.schema import StatementCreate


async def list_statements(offset: int = 0, limit: int = 20) -> list[Statement]:
    result = await db.session.execute(select(Statement).offset(offset).limit(limit))
    return result.scalars().all()


async def create_statement(data: StatementCreate) -> Statement:
    statement = Statement(**data.model_dump())
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
