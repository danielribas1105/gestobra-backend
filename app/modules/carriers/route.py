import uuid

from fastapi import APIRouter, Depends, HTTPException
from app.modules.auth.service import get_current_user
from app.modules.carriers.schema import CarrierResponse
from app.modules.user.model import User
from app.modules.carriers import service

router = APIRouter(prefix="/carriers", tags=["Carriers"])


@router.get("", response_model=list[CarrierResponse])
async def list_carriers(
    offset: int = 0, limit: int = 20, user: User = Depends(get_current_user)
):
    return await service.list_carriers(offset, limit)
