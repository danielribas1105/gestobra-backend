import uuid

from fastapi import HTTPException
from fastapi_async_sqlalchemy import db
from sqlalchemy import select
from app.modules.materials.model import Material
from app.modules.materials.schema import MaterialCreate, MaterialUpdate


async def list_materials(offset: int = 0, limit: int = 20) -> list[Material]:
    result = await db.session.execute(select(Material).offset(offset).limit(limit))
    return result.scalars().all()


async def create_material(data: MaterialCreate) -> Material:
    material = Material(**data.model_dump())
    db.session.add(material)
    await db.session.commit()
    await db.session.refresh(material)
    return material


async def get_material_by_id(material_id: uuid.UUID) -> Material | None:
    result = await db.session.execute(
        select(Material).where(Material.id == material_id)
    )
    return result.scalars().first()


async def update(material_id: uuid.UUID, data: MaterialUpdate) -> Material:
    material = await get_material_by_id(material_id)
    if not material:
        raise HTTPException(status_code=404, detail="Material não encontrado")
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(material, field, value)
    await db.session.commit()
    await db.session.refresh(material)
    return material


async def delete(material_id: uuid.UUID) -> None:
    material = await get_material_by_id(material_id)
    if not material:
        raise HTTPException(status_code=404, detail="Material não encontrado")
    await db.session.delete(material)
    await db.session.commit()
