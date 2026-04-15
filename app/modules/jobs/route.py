import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from app.modules.auth.dependencies import require_admin
from app.modules.auth.service import get_current_user
from app.modules.user.model import User
from app.modules.jobs.schema import JobCreate, JobResponse, JobUpdate
from app.modules.jobs import service

router = APIRouter(prefix="/jobs", tags=["Jobs"])


@router.get("", response_model=list[JobResponse])
async def list_jobs(
    offset: int = 0, limit: int = 20, user: User = Depends(get_current_user)
):
    return await service.list_jobs(offset, limit)


@router.post("/", response_model=JobResponse, status_code=201)
async def create_job(job: JobCreate, user: User = Depends(require_admin)):
    return await service.create_job(job, created_by=user.id)


@router.get("/{job_id}", response_model=JobResponse)
async def get_job(job_id: uuid.UUID, user: User = Depends(get_current_user)):
    job = await service.get_job_by_id(job_id)
    if not job:
        raise HTTPException(
            status_code=404, detail="Movimentação entre obras, não encontrada"
        )
    return job


@router.put("/{job_id}", response_model=JobResponse)
async def update_job(
    job_id: uuid.UUID,
    data: JobUpdate,
    user: User = Depends(get_current_user),
):
    return await service.update(job_id, data)


@router.delete("/{job_id}", status_code=204)
async def delete_job(job_id: uuid.UUID, user: User = Depends(get_current_user)):
    await service.delete(job_id)
