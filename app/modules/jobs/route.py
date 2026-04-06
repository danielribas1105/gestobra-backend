from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlmodel import select
from app.db.database import get_session
from app.modules.jobs.model import Job

router = APIRouter(prefix="/job", tags=["jobs"])


@router.post("/")
def create_job(job: Job, session: Session = Depends(get_session)):
    session.add(job)
    session.commit()
    session.refresh(job)
    return job


@router.get("/")
def list_jobs(session: Session = Depends(get_session)):
    jobs = session.exec(select(Job)).all()
    return jobs
