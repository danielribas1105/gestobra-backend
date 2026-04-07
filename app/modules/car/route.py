from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, selectinload
from sqlmodel import select
from app.db.database import get_db
from app.modules.car.model import Car
from app.modules.car import schema
from app.modules.user.model import User

router = APIRouter(prefix="/car", tags=["cars"])


@router.post("/", response_model=schema.CarResponse)
def create_car(car: schema.CarCreate, session: Session = Depends(get_db)):
    db_car = Car(**car.dict())
    session.add(db_car)
    session.commit()
    session.refresh(db_car)
    return db_car


@router.get("/", response_model=list[schema.CarResponse])
def list_cars(session: Session = Depends(get_db)):
    statement = select(Car).options(selectinload(Car.driver))
    cars = session.exec(statement).all()
    return cars


@router.get("/{id}", response_model=schema.CarResponse)
def get_car(id: str, session: Session = Depends(get_db)):
    statement = select(Car).where(Car.id == id).options(selectinload(Car.driver))
    car = session.exec(statement).first()

    if not car:
        raise HTTPException(status_code=404, detail="Car not found")

    return car


@router.patch("/{id}/assign-driver", response_model=schema.CarResponse)
def assign_driver(id: str, driver_id: str, session: Session = Depends(get_db)):
    # Verifica se o carro existe
    car = session.get(Car, id)
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")

    # Verifica se o user existe
    user = session.get(User, driver_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Atualiza o motorista
    car.driver_id = driver_id
    session.add(car)
    session.commit()
    session.refresh(car)

    return car
