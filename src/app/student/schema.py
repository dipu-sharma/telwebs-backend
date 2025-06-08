from re import search
from pydantic import BaseModel, Field
from typing import Optional


class MarksSchema(BaseModel):
    id: Optional[int] = None
    mark: int = Field(description="Mark", default=None)
    subject_name: str = Field(description="Subject name", default=None)
    student_id: int = Field(description="Student id", default=None)
    teacher_id: int = Field(description="Teacher id", default=None)

    class Config:
        from_attributes=True
        extra_json_attributes = {
            "id": "id",
            "mark": "mark",
            "subject_name": "subject_name",
            "student_id": "student_id",
            "teacher_id": "teacher_id",
        }


class MarksCreateSchema(BaseModel):
    mark: int = Field(description="Mark", default=None)
    subject_name: str = Field(description="Subject name", default=None)

    class Config:
        from_attributes=True
        extra_json_attributes = {
            "mark": "mark",
            "subject_name": "subject_name",
        }


class MarksUpdateSchema(BaseModel):
    id: Optional[int] = Field(description="Mark id", default=None)
    mark: int = Field(description="Mark", default=None)
    subject_name: str = Field(description="Subject name", default=None)
    teacher_id: int = Field(description="Teacher id", default=None)

    class Config:
        from_attributes=True
        extra_json_attributes = {
            "mark": "mark",
            "subject_name": "subject_name",
            "teacher_id": "teacher_id",
        }


class StudentSchema(BaseModel):
    id: Optional[int] = None
    student_name: str = Field(description="Student name", default=None)
    teacher_id: int = Field(description="Teacher id", default=None)
    subject_marks: list[MarksSchema] = Field(description="Marks", default=None)

    class Config:
        from_attributes=True
        


class StudentCreateSchema(BaseModel):
    student_name: str = Field(description="Student name", default=None)
    teacher_id: int = Field(description="Teacher id", default=None)
    subject_marks: list[MarksCreateSchema] = Field(description="Marks", default=None)

    class Config:
        from_attributes=True
        extra_json_attributes = {
            "student_name": "student_name",
            "teacher_id": "teacher_id",
        }


class StudentUpdateSchema(BaseModel):

    student_name: str = Field(description="Student name", default=None)
    teacher_id: int = Field(description="Teacher id", default=None)
    subject_marks: list[MarksUpdateSchema] = Field(description="Marks", default=None)

    class Config:
        from_attributes=True
        extra_json_attributes = {
            "student_name": "student_name",
            "teacher_id": "teacher_id",
        }



class StudentFilterSchema(BaseModel):
    search: Optional[str] = None
    limit: Optional[int] = 10
    skip: Optional[int] = 0

    class Config:
        from_attributes=True
