import uuid
from sqlalchemy.orm import Session
from fastapi_async_sqlalchemy import db
from sqlmodel import select
from . import model, schema


def create_statement(db: Session, statement: schema.StatementCreate):
    db_statement = model.Statement(**statement.dict())
    db.add(db_statement)
    db.commit()
    db.refresh(db_statement)
    return db_statement

def list_statements(db: Session):
    return db.query(model.Statement).all()

async def get_statement_by_id(id: uuid.UUID | str | None):
    return await db.session.get(model.Statement, id)
