from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.db import get_db
from schemas.car import CarCreate, CarUpdate, CarResponse
from models.car import Car
from utils.jwt_handler import decode_access_token
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

router = APIRouter(tags=["Cars"])


def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_access_token(token)
    user_id = payload.get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid authentication token")
    return user_id


@router.post("", response_model=CarResponse)
def create_car(
    car: CarCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    new_car = Car(
        user_id=user_id,
        brand=car.brand,
        model=car.model,
        year=car.year,
        fuel_type=car.fuel_type,
        engine_size=car.engine_size
    )
    db.add(new_car)
    db.commit()
    db.refresh(new_car)
    return new_car


@router.get("", response_model=list[CarResponse])
def get_cars(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    return db.query(Car).filter(Car.user_id == user_id).all()


@router.get("/{car_id}", response_model=CarResponse)
def get_car_by_id(
    car_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    car = db.query(Car).filter(Car.id == car_id, Car.user_id == user_id).first()

    if not car:
        raise HTTPException(status_code=404, detail="Car not found")

    return car


@router.put("/{car_id}", response_model=CarResponse)
def update_car(
    car_id: int,
    car_data: CarUpdate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    car = db.query(Car).filter(Car.id == car_id, Car.user_id == user_id).first()

    if not car:
        raise HTTPException(status_code=404, detail="Car not found")

    for field, value in car_data.dict(exclude_unset=True).items():
        setattr(car, field, value)

    db.commit()
    db.refresh(car)
    return car


@router.delete("/{car_id}")
def delete_car(
    car_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    car = db.query(Car).filter(Car.id == car_id, Car.user_id == user_id).first()

    if not car:
        raise HTTPException(status_code=404, detail="Car not found")

    db.delete(car)
    db.commit()

    return {"message": "Car deleted successfully"}
