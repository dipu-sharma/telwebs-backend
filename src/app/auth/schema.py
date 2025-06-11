from pydantic import BaseModel, EmailStr, Field
import enum
from datetime import datetime
from typing import Any, Dict, Optional, List
from fastapi import status

class RoleEnum(str, enum.Enum):
    student = "student"
    teacher = "teacher"

class UserSchema(BaseModel):
    id: Optional[int] = None
    email: EmailStr
    role: Optional[RoleEnum] = None

    class Config:
        from_attributes=True
        extra_json_attributes = {
            "email": "email",
            "role": "student"
        }


class LoginSchema(BaseModel):
    email: EmailStr = Field(description="User email")
    password: str = Field(description="User password")

    class Config:
        from_attributes=True
        extra_json_attributes = {
            "email": "email",
            "password": "password"
        }


class RegisterSchema(BaseModel):
    email: EmailStr = Field(description="User email")
    password: str = Field(description="User password")
    confirm_password: str = Field(description="Confirm password")
    role: RoleEnum = Field(description="User role", default="student")

    class Config:
        from_attributes=True
        extra_json_attributes = {
            "email": "email",
            "password": "password",
            "confirm_password": "confirm_password",
            "role": "student"
        }



class ResponseModel(BaseModel):
    """
    Base Response Model
    """
    data: Any = {}
    status_code: int = status.HTTP_200_OK
    success: bool = True
    message: str = 'Request handled successfully'
    changes: List[str] = []


class ErrorResponseModel(BaseModel):
    """
    Base Error Model
    """
    error: Any = {}
    status_code: int = status.HTTP_400_BAD_REQUEST
    success: bool = False
    message: str = 'Request could not be processed'


class ExistResponseModel(BaseModel):
    """
    Existing Record Show
    """
    data: Any = {}
    status_code: int = status.HTTP_226_IM_USED
    success: bool = True
    message: str = None
