from pydantic import BaseModel, Field, EmailStr
from enum import Enum
from datetime import datetime
from typing import Optional


class UserRole(str, Enum):
    USER = "User"
    ADMIN = "Admin"


class UserBaseModel(BaseModel):
    email: EmailStr
    first_name: str = Field(..., min_length=1)
    last_name: str = Field(..., min_length=1)
    address: str = Field(..., min_length=1)
    phone_number: str


class User(UserBaseModel):
    id: str
    user_role: UserRole = Field(default=UserRole.USER)
    email_verified: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class CreateUser(UserBaseModel):
    password: str
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class LoginUser(BaseModel):
    email: EmailStr
    password: str


class LoginUserResponse(BaseModel):
    message: str = Field(default="Login successful", min_length=1)
    access_token: str = Field(..., min_length=1)
    refresh_token: str = Field(..., min_length=1)
    user: User


class UpdateUser(BaseModel):
    first_name: Optional[str] = Field(None, min_length=1)
    last_name: Optional[str] = Field(None, min_length=1)
    address: Optional[str] = Field(None, min_length=1)
    phone_number: Optional[str] = Field(None)
    updated_at: datetime = Field(default_factory=datetime.now)
