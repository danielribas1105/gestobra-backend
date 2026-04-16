import uuid

from fastapi import APIRouter, Depends, HTTPException
from app.modules.auth.service import get_current_user
from app.modules.materials.schema import (
    MaterialCreate,
    MaterialResponse,
    MaterialUpdate,
)
from app.modules.materials import service
from app.modules.user.model import User

router = APIRouter(prefix="/materials", tags=["Materials"])


@router.get("", response_model=list[MaterialResponse])
async def list_materials(
    offset: int = 0, limit: int = 20, user: User = Depends(get_current_user)
):
    return await service.list_materials(offset, limit)


@router.post("", response_model=MaterialResponse, status_code=201)
async def create_material(
    material: MaterialCreate, user: User = Depends(get_current_user)
):
    return await service.create_material(material)


@router.get("/{material_id}", response_model=MaterialResponse)
async def get_material(material_id: uuid.UUID, user: User = Depends(get_current_user)):
    material = await service.get_material_by_id(material_id)
    if not material:
        raise HTTPException(status_code=404, detail="Material não encontrado")
    return material


@router.put("/{material_id}", response_model=MaterialResponse)
async def update_material(
    material_id: uuid.UUID,
    data: MaterialUpdate,
    user: User = Depends(get_current_user),
):
    return await service.update(material_id, data)


@router.delete("/{material_id}", status_code=204)
async def delete_material(
    material_id: uuid.UUID, user: User = Depends(get_current_user)
):
    await service.delete(material_id)
