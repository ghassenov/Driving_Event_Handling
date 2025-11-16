from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from utils.jwt_handler import decode_access_token
from database.db import get_db
from models.models import Trip

router = APIRouter()

@router.post("/save")
def save_trip(token: str, score: float, db: Session = Depends(get_db)):
    try:
        payload = decode_access_token(token)
        user_id = payload["user_id"]
    except:
        raise HTTPException(401, "Invalid token")

    trip = Trip(user_id=user_id, score=score)
    db.add(trip)
    db.commit()

    return {"message": "Trip saved", "score": score}
