from pydantic import BaseModel, EmailStr, Field
from typing import Optional
import enum

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
