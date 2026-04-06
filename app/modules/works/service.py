from sqlalchemy.orm import Session
from . import model, schema


def create_work(db: Session, work: schema.WorkCreate) -> model.Work:
    new_work = model.Work(**work.dict())
    db.add(new_work)
    db.commit()
    db.refresh(new_work)
    return new_work


def list_works(db: Session):
    return db.query(model.Work).all()
