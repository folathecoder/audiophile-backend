from fastapi import Depends, HTTPException
from pydantic import EmailStr
from app.auth.bearer_auth import AccessTokenBearer
from starlette import status

access_token_bearer = AccessTokenBearer()


async def user_authorisation_check_by_email(
    user_email: EmailStr, access=Depends(access_token_bearer)
) -> EmailStr:
    current_user_email = access["user"]["email"]

    if user_email != current_user_email:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"User with email '{current_user_email}' cannot perform operations on this profile",
        )

    return current_user_email


async def user_authorisation_check_by_id(
    user_id: str, access=Depends(access_token_bearer)
) -> EmailStr:
    current_user_id = access["user"]["id"]

    if user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"User with id '{current_user_id}' cannot perform operations on this profile",
        )

    return current_user_id
