
from pydantic import BaseModel, Field
from typing import Optional, List
from src.app.student.schema import StudentSchema

class TeacherSchema(BaseModel):
    id: Optional[int] = None
    teacher_name: str = Field(description="Teacher name", default=None)
    subject: str = Field(description="Subject", default=None)
    user_id: int = Field(description="User id", default=None)
    students: Optional[List[StudentSchema]] = Field(default=[])

    class Config:
        from_attributes=True
        extra_json_attributes = {
            "id": "id",
            "teacher_name": "teacher_name",
            "subject": "subject",
            "user_id": "user_id",
        }


class CreateTeacherSchema(TeacherSchema):
    pass

class UpdateTeacherSchema(TeacherSchema):
    pass