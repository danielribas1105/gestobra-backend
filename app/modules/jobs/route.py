import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlmodel import select
from app.db.database import get_db
from app.modules.auth.service import get_current_user
from app.modules.user.model import User
from app.modules.jobs.model import Job
from app.modules.jobs.schema import JobCreate, JobResponse
from app.modules.jobs import service

router = APIRouter(prefix="/jobs", tags=["Jobs"])


@router.get("", response_model=list[JobResponse])
async def list_jobs(
    offset: int = 0, limit: int = 20, user: User = Depends(get_current_user)
):
    return await service.list_jobs(offset, limit)


@router.post("/", response_model=JobResponse, status_code=201)
async def create_job(job: JobCreate, user: User = Depends(get_current_user)):
    return await service.create_job(job)


@router.get("/{job_id}", response_model=JobResponse)
async def get_job(job_id: uuid.UUID, user: User = Depends(get_current_user)):
    job = await service.get_job_by_id(job_id)
    if not job:
        raise HTTPException(
            status_code=404, detail="Movimentação entre obras, não encontrada"
        )
    return job
