from pydantic import BaseModel

class UserCreate(BaseModel):
    full_name: str
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    full_name: str
    email: str

    class Config:
        orm_mode = True

class TokenResponse(BaseModel):
    access_token: str
    user: UserResponse

class SensorRow(BaseModel):
    acc_x: float
    acc_y: float
    acc_z: float
    gyro_x: float
    gyro_y: float
    gyro_z: float
    mag_x: float
    mag_y: float
    mag_z: float

class TripData(BaseModel):
    sensors: list[SensorRow]


class PredictionResponse(BaseModel):
    score: float
    events: list[int]
