from datetime import datetime, timedelta
import jwt
from config.config import JWT_SECRET, JWT_ALGORITHM

def create_access_token(data: dict, expires_minutes=60):
    payload = data.copy()
    payload["exp"] = datetime.utcnow() + timedelta(minutes=expires_minutes)
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

def decode_access_token(token: str):
    return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
