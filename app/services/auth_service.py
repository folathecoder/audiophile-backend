from app.models.user import *
from fastapi import HTTPException
from starlette import status
from datetime import timedelta, datetime
from app.services.user_service import UserService
from app.db.collections import users_collection
from app.schemas.user import user_data_schema
from app.core.config import settings
from app.auth.password_auth import hash_password, verify_password
from app.auth.token_auth import create_access_token


class AuthService:

    @staticmethod
    async def register_user(register_user_data: CreateUser) -> User:
        new_user = register_user_data.model_dump()
        user_email = new_user["email"]

        if await UserService.user_exist(user_email):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"User with email address '{user_email}' already exists, try logging in instead",
            )

        new_user.update(
            {
                "user_role": await UserService.assign_user_role(user_email),
                "email_verified": False,
                "password": hash_password(new_user["password"]),
            }
        )

        response = users_collection.insert_one(new_user)
        new_user["_id"] = response.inserted_id

        return user_data_schema(new_user)

    @staticmethod
    async def login_user(login_user_data: LoginUser) -> LoginUserResponse:
        login_data = login_user_data.model_dump()
        user_email = login_data["email"]
        user_password = login_data["password"]

        if not await UserService.user_exist(user_email):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"User with email address '{user_email}' does not exist",
            )

        user = await UserService.get_user_by_email(user_email)

        if not verify_password(user_password, user["password"]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"The password provided is incorrect: {user_email}",
            )

        user_data = {"email": user_email, "id": str(user["_id"])}

        access_token = create_access_token(user_data=user_data)
        refresh_token = create_access_token(
            user_data=user_data,
            refresh=True,
            expiry=timedelta(days=int(settings.REFRESH_TOKEN_EXPIRY)),
        )

        return {
            "message": f"User with email {user_email} has been logged in successfully",
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": user_data_schema(user),
        }

    @staticmethod
    async def logout_user() -> None:
        pass

    @staticmethod
    async def reset_password() -> None:
        pass

    @staticmethod
    async def confirm_password_reset() -> None:
        pass

    @staticmethod
    async def send_email_verification() -> None:
        pass

    @staticmethod
    async def confirm_email_verification() -> None:
        pass
