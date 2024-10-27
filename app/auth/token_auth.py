import jwt
import uuid
from fastapi import HTTPException
from datetime import timedelta, datetime
from starlette import status
from app.core.config import settings


def create_access_token(
    user_data: dict, expiry: timedelta = None, refresh: bool = False
):
    payload = {
        "user": user_data,
        "exp": (
            datetime.now() + expiry
            if expiry is not None
            else datetime.now() + timedelta(seconds=int(settings.ACCESS_TOKEN_EXPIRY))
        ),
        "jti": str(uuid.uuid4()),
        "refresh": refresh,
    }

    return jwt.encode(
        payload=payload,
        key=settings.JWT_SECRET,
        algorithm=settings.JWT_ALGORITHM,
    )


def decode_access_token(token: str) -> dict:
    try:
        return jwt.decode(
            jwt=token, key=settings.JWT_SECRET, algorithms=settings.JWT_ALGORITHM
        )
    except jwt.PyJWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Error decoding access token: {str(e)}",
        )
