from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from app.auth.token_auth import decode_access_token
from app.core.logger import logger
from starlette import status
from typing import Optional


class AccessTokenBearer(HTTPBearer):

    def __init__(self, auto_error=True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> Optional[dict]:
        creds: HTTPAuthorizationCredentials = await super().__call__(request)
        token = creds.credentials if creds else None

        logger.info("Starting access token verification")

        if not token:
            logger.warning("Authorization token not provided in request")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authorization token not provided",
            )

        try:
            token_data = decode_access_token(token)
        except Exception as e:
            logger.error(f"Token decoding error: {e}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token",
            )

        if token_data.get("refresh"):
            logger.warning("Received a refresh token instead of an access token")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Please provide an access token, not a refresh token",
            )

        logger.info(f"Token successfully verified: {token_data}")
        return token_data
