from sqlalchemy.orm import Session
from . import model, schema


def create_job(db: Session, job: schema.JobCreate):
    db_job = model.Job(**job.dict())
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job


def list_jobs(db: Session):
    return db.query(model.Job).all()
