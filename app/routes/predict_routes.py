from fastapi import APIRouter
from schemas.schemas import TripData
from utils.predict import predict_trip

router = APIRouter()

@router.post("/")
def predict(trip: TripData):
    score, events = predict_trip(trip)
    return {"score": score, "events": events}
