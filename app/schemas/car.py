from pydantic import BaseModel
from enum import Enum
from typing import Optional

class FuelType(str, Enum):
    diesel = "diesel"
    petrol = "petrol"
    hybrid = "hybrid"
    electric = "electric"

class CarBase(BaseModel):
    brand: str
    model: str
    year: Optional[int] = None
    fuel_type: FuelType
    engine_size: Optional[float] = None  


class CarCreate(CarBase):
    pass


class CarResponse(CarBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True
        
class CarUpdate(BaseModel):
    brand: Optional[str]
    model: Optional[str]
    year: Optional[int]
    fuel_type: Optional[FuelType]
    engine_size: Optional[float]
