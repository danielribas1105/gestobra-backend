from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlmodel import select
from app.db.database import get_db
from app.modules.works.model import Work

router = APIRouter(prefix="/work", tags=["works"])


@router.post("/")
def create_work(work: Work, session: Session = Depends(get_db)):
    session.add(work)
    session.commit()
    session.refresh(work)
    return work


@router.get("/")
def list_works(session: Session = Depends(get_db)):
    works = session.exec(select(Work)).all()
    return works
