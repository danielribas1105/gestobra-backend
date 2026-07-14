import uuid

from fastapi import APIRouter, Depends, HTTPException
from app.modules.auth.service import get_current_user
from app.modules.user.model import User
from app.modules.statements.schema import (
    StatementCreate,
    StatementResponse,
    StatementUpdate,
    StatementsCount,
)
from app.modules.statements import service

router = APIRouter(prefix="/statements", tags=["Statements"])


# 1. Rotas estáticas primeiro
@router.get("/without-job", response_model=list[StatementResponse])
async def list_statements_without_job(
    offset: int = 0, limit: int = 20, user: User = Depends(get_current_user)
):
    return await service.list_statements_without_job(offset, limit)


@router.get("/count-statements", response_model=StatementsCount)
async def get_count_statements(user: User = Depends(get_current_user)):
    return await service.count_statements()


@router.get("/by-job/{job_id}", response_model=StatementResponse)
async def get_statement_by_job(
    job_id: uuid.UUID, user: User = Depends(get_current_user)
):
    statement = await service.get_statement_by_job_id(job_id)
    if not statement:
        raise HTTPException(status_code=404, detail="Pagamento não encontrado")
    return statement


# 2. Rotas raiz
@router.get("", response_model=list[StatementResponse])
async def list_all_statements(
    offset: int = 0, limit: int = 20, user: User = Depends(get_current_user)
):
    return await service.list_statements(offset, limit)


@router.post("", response_model=StatementResponse, status_code=201)
async def create_statement(
    statement: StatementCreate, user: User = Depends(get_current_user)
):
    return await service.create_statement(statement)


# 3. Rotas com parâmetro dinâmico por último
@router.get("/{statement_id}", response_model=StatementResponse)
async def get_statement(
    statement_id: uuid.UUID, user: User = Depends(get_current_user)
):
    statement = await service.get_statement_by_id(statement_id)
    if not statement:
        raise HTTPException(status_code=404, detail="Manifesto não encontrado")
    return statement


@router.put("/{statement_id}", response_model=StatementResponse)
async def update_statement(
    statement_id: uuid.UUID,
    data: StatementUpdate,
    user: User = Depends(get_current_user),
):
    statement = await service.get_statement_by_id(statement_id)
    if not statement:
        raise HTTPException(status_code=404, detail="Manifesto não encontrado")
    return await service.update(statement_id, data)


@router.delete("/{statement_id}", status_code=204)
async def delete_statement(
    statement_id: uuid.UUID, user: User = Depends(get_current_user)
):
    await service.delete(statement_id)
