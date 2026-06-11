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
    jobs = await service.list_jobs(offset, limit)
    return [
        JobResponse(
            **job.model_dump(),
            origin_name=job.origin_work.name if job.origin_work else None,
            destiny_name=job.destiny_work.name if job.destiny_work else None,
            car_license=job.car.license if job.car else None,
            driver_name=job.driver.name if job.driver else None,
            creator_name=job.creator.name if job.creator else None,
            statement_code=job.statement.code if job.statement else None,
            material_name=(
                job.statement.material.name
                if job.statement and job.statement.material
                else None
            ),
            value_m3=job.statement.material.value_m3 if job.statement else None,
            m3=job.statement.m3 if job.statement else None,
        )
        for job in jobs
    ]


@router.post("", response_model=JobResponse, status_code=201)
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
    job_id: uuid.UUID, data: JobUpdate, user: User = Depends(require_admin)
):
    job = await service.get_job_by_id(job_id)
    if not job:
        raise HTTPException(
            status_code=404, detail="Movimentação entre obras não encontrada"
        )
    return await service.update(job_id, data)


@router.delete("/{job_id}", status_code=204)
async def delete_job(job_id: uuid.UUID, user: User = Depends(require_admin)):
    job = await service.get_job_by_id(job_id)
    if not job:
        raise HTTPException(
            status_code=404, detail="Movimentação entre obras não encontrada"
        )
    await service.delete(job_id)


@router.get("/by-work/{work_id}", response_model=list[JobResponse])
async def list_jobs_by_work_origin(
    work_id: uuid.UUID, user: User = Depends(get_current_user)
):
    jobs = await service.list_jobs_by_work_origin(work_id)
    return [
        JobResponse(
            **job.model_dump(),
            origin_name=job.origin_work.name if job.origin_work else None,
            destiny_name=job.destiny_work.name if job.destiny_work else None,
            car_license=job.car.license if job.car else None,
            driver_name=job.driver.name if job.driver else None,
            creator_name=job.creator.name if job.creator else None,
            statement_code=job.statement.code if job.statement else None,
            material_name=(
                job.statement.material.name
                if job.statement and job.statement.material
                else None
            ),
            value_m3=job.statement.material.value_m3 if job.statement else None,
            m3=job.statement.m3 if job.statement else None,
        )
        for job in jobs
    ]
