from fastapi import APIRouter, HTTPException
from app.models.user import *
from app.services.auth_service import AuthService
from starlette import status

auth_router = APIRouter()


@auth_router.post("/register", status_code=status.HTTP_200_OK, response_model=User)
async def register_user(register_user_data: CreateUser):
    try:
        return await AuthService.register_user(register_user_data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"User not registered: {str(e)}",
        )


@auth_router.post(
    "/login", status_code=status.HTTP_200_OK, response_model=LoginUserResponse
)
async def login_user(login_user_data: LoginUser):
    try:
        return await AuthService.login_user(login_user_data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"User cannot be logged in: {str(e)}",
        )


@auth_router.post("/logout")
async def logout_user():
    return None


@auth_router.put("/password/reset")
async def reset_password():
    return None


@auth_router.post("/password/reset/confirm")
async def confirm_password_reset():
    return None


@auth_router.post("/email/verify")
async def send_email_verification():
    return None


@auth_router.post("/email/verify/confirm")
async def confirm_email_verification():
    return None
