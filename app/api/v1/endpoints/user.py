from fastapi import APIRouter, HTTPException, Depends
from pydantic import EmailStr
from starlette import status
from app.models.user import User, UpdateUser
from app.services.user_service import UserService
from app.auth.bearer_auth import AccessTokenBearer
from app.schemas.user import user_data_schema
from app.auth.check_auth import user_authorisation_check_by_email

user_router = APIRouter()
access_token_bearer = AccessTokenBearer()


@user_router.get(
    "/profile/{user_email}", status_code=status.HTTP_200_OK, response_model=User
)
async def get_user_profile(
    user_email: EmailStr, current_user=Depends(user_authorisation_check_by_email)
):
    try:
        user = await UserService.get_user_by_email(user_email)
        return user_data_schema(user)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with email '{current_user}', could not be found: {e}",
        )


@user_router.patch(
    "/profile/{user_email}", status_code=status.HTTP_200_OK, response_model=User
)
async def update_user_profile(
    user_email: EmailStr,
    update_user_data: UpdateUser,
    current_user=Depends(user_authorisation_check_by_email),
):
    try:
        return await UserService.update_user_by_email(user_email, update_user_data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User profile '{current_user}' was not updated: {e}",
        )


@user_router.get("/orders")
async def get_user_orders():
    pass
