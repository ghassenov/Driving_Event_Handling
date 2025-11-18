from datetime import datetime, timedelta
import jwt
from config.config import JWT_SECRET, JWT_ALGORITHM
from fastapi import HTTPException, status

def create_access_token(data: dict, expires_minutes=60):
    try:
        payload = data.copy()
        payload["exp"] = datetime.utcnow() + timedelta(minutes=expires_minutes)
        token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
        
        if isinstance(token, bytes):
            token = token.decode('utf-8')
            
        return token
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Token creation failed: {str(e)}"
        )

def decode_access_token(token: str):
    try:
        # Basic validation - check if token has the right structure
        if not token or token.count('.') != 2:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token format"
            )
        
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )
    except jwt.DecodeError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )