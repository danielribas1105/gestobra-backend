import uuid

from fastapi import APIRouter, Depends, HTTPException
from app.modules.auth.service import get_current_user
from app.modules.user.model import User
from app.modules.works.schema import WorkCreate, WorkResponse, WorkUpdate
from app.modules.works import service

router = APIRouter(prefix="/works", tags=["Works"])


@router.get("", response_model=list[WorkResponse])
async def list_works(
    offset: int = 0, limit: int = 20, user: User = Depends(get_current_user)
):
    return await service.list_works(offset, limit)


@router.post("", response_model=WorkResponse, status_code=201)
async def create_work(work: WorkCreate, user: User = Depends(get_current_user)):
    return await service.create_work(work)


@router.get("/{work_id}", response_model=WorkResponse)
async def get_work(work_id: uuid.UUID, user: User = Depends(get_current_user)):
    work = await service.get_work_by_id(work_id)
    if not work:
        raise HTTPException(status_code=404, detail="Obra não encontrada")
    return work


@router.put("/{work_id}", response_model=WorkResponse)
async def update_work(
    work_id: uuid.UUID,
    data: WorkUpdate,
    user: User = Depends(get_current_user),
):
    return await service.update(work_id, data)


@router.delete("/{work_id}", status_code=204)
async def delete_work(work_id: uuid.UUID, user: User = Depends(get_current_user)):
    await service.delete(work_id)
