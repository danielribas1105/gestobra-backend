from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, selectinload
from sqlmodel import select
from app.db.database import get_session
from app.modules.statements.model import Statement
from app.modules.statements import schema

router = APIRouter(prefix="/statement", tags=["statements"])

@router.post("/", response_model=schema.StatementOut)
def create_statement(statement: schema.StatementCreate, session: Session = Depends(get_session)):
    db_statement = Statement(**statement.dict())
    session.add(db_statement)
    session.commit()
    session.refresh(db_statement)
    return db_statement

@router.get("/", response_model=list[schema.StatementOut])
def list_statements(session: Session = Depends(get_session)):
    statement = select(Statement)
    statements = session.exec(statement).all()
    return statements

@router.get("/{id}", response_model=schema.StatementOut)
def get_statement(id: str, session: Session = Depends(get_session)):
    statement = (
        select(Statement)
        .where(Statement.id == id)
    )
    statement = session.exec(statement).first()

    if not statement:
        raise HTTPException(status_code=404, detail="User not found")

    return statement
