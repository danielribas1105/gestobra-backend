from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlmodel import select
from app.db.database import get_session
from app.modules.works.model import Work

router = APIRouter(prefix="/work", tags=["works"])

@router.post("/")
def create_work(work: Work, session: Session = Depends(get_session)):
    session.add(work)
    session.commit()
    session.refresh(work)
    return work

@router.get("/")
def list_works(session: Session = Depends(get_session)):
    works = session.exec(select(Work)).all()
    return works
