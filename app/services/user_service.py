from app.models.user import *
from pydantic import EmailStr
from app.db.collections import users_collection
from app.core.config import settings
from fastapi import HTTPException
from starlette import status

from app.schemas.user import user_data_schema


class UserService:

    @staticmethod
    async def get_user_by_email(email: EmailStr) -> User:
        user = users_collection.find_one({"email": email})

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with email '{email}', could not be found",
            )

        return user

    @staticmethod
    async def update_user_by_email(
        email: EmailStr, update_user_data: UpdateUser
    ) -> User:
        update_user_obj = update_user_data.model_dump(exclude_unset=True)

        if not await UserService.user_exist(email):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with email '{email}', could not be found",
            )

        update_user_obj["updated_at"] = datetime.now()
        response = users_collection.update_one(
            {"email": email}, {"$set": update_user_obj}
        )

        if response.modified_count == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"User profile '{email}' was not updated",
            )

        user = await UserService.get_user_by_email(email)

        return user_data_schema(user)

    @staticmethod
    async def user_exist(email: EmailStr) -> bool:
        return await UserService.get_user_by_email(email) is not None

    @staticmethod
    async def assign_user_role(email: EmailStr) -> UserRole:
        if not settings.ADMIN_EMAIL_EXTENSION:
            raise ValueError("ADMIN_EMAIL_EXTENSION is not set in settings.")

        return (
            UserRole.ADMIN if settings.ADMIN_EMAIL_EXTENSION in email else UserRole.USER
        )
