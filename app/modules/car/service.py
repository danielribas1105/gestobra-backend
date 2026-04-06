from sqlalchemy.orm import Session
from . import model, schema


def create_car(db: Session, car: schema.CarCreate):
    db_car = model.Car(**car.dict())
    db.add(db_car)
    db.commit()
    db.refresh(db_car)
    return db_car


def list_cars(db: Session):
    return db.query(model.Car).all()
