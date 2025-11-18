from sqlalchemy import Column,Enum, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from database.db import Base
import enum

class FuelType(enum.Enum):
    diesel = "diesel"
    petrol = "petrol"
    hybrid = "hybrid"
    electric = "electric"
class Car(Base):
    __tablename__ = "cars"

    id = Column(Integer, primary_key=True, index=True)
    brand = Column(String, nullable=False)
    model = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    engine_size = Column(Float, nullable=True)
    fuel_type = Column(Enum(FuelType), nullable=True)      
    user_id = Column(Integer, ForeignKey("users.id"))
    
    user = relationship("User", back_populates="cars")
