from unittest import skip
from src.modals.modal import Student, SubjectMark
from src.database.db_config import get_db
from sqlalchemy.orm import Session
from src.app.student.schema import (
    StudentCreateSchema,
    StudentSchema,
    StudentUpdateSchema,
    MarksCreateSchema,
    MarksSchema,
    MarksUpdateSchema,
    StudentFilterSchema,
)

from src.app.auth.schema import ResponseModel, ErrorResponseModel, ExistResponseModel
from fastapi import Depends, status
from sqlalchemy.orm import joinedload
from fastapi.encoders import jsonable_encoder


async def create_or_update_student(
    payload: StudentCreateSchema, db: Session = Depends(get_db)
):
    # First check if student with same name and teacher exists
    existing_student = (
        db.query(Student)
        .options(joinedload(Student.subject_marks))
        .filter(
            Student.student_name == payload.student_name,
            Student.teacher_id == payload.teacher_id,
        )
        .first()
    )

    if existing_student:
        # Check each subject mark to prevent duplicates
        existing_subjects = {mark.subject_name for mark in existing_student.subject_marks}
        new_subjects = {mark.subject_name for mark in payload.subject_marks}
        
        # Find subjects that already exist
        duplicate_subjects = existing_subjects & new_subjects
        if duplicate_subjects:
            return ErrorResponseModel(error=f"{', '.join(duplicate_subjects)} already exist for this student")
        
        # Add only new subject marks
        for mark in payload.subject_marks:
            new_mark = SubjectMark(
                mark=mark.mark,
                subject_name=mark.subject_name,
                student_id=existing_student.id,
                teacher_id=existing_student.teacher_id
            )
            existing_student.subject_marks.append(new_mark)
        
        db.commit()
        db.refresh(existing_student)
        return ResponseModel(data=StudentSchema.from_orm(existing_student), message="Student marks updated successfully")

    # Create new student if doesn't exist
    student_data = {
        "student_name": payload.student_name,
        "teacher_id": payload.teacher_id
    }
    
    new_student = Student(**student_data)
    db.add(new_student)
    db.flush()  # Get the new student ID
    
    # Add all subject marks
    for mark in payload.subject_marks:
        new_mark = SubjectMark(
            mark=mark.mark,
            subject_name=mark.subject_name,
            student_id=new_student.id,
            teacher_id=new_student.teacher_id
        )
        db.add(new_mark)
    
    db.commit()
    db.refresh(new_student)
    return ResponseModel(data=StudentSchema.from_orm(new_student), message="Student created successfully")


async def update_student(student_id: int, payload: StudentUpdateSchema, db: Session = Depends(get_db)):
    # Load the student with their marks in a single query
    existing = (
        db.query(Student)
        .options(joinedload(Student.subject_marks))
        .filter(Student.id == student_id)
        .first()
    )

    if not existing:
        return ErrorResponseModel(error="Student not found")
    existing_marks = {mark.id: mark for mark in existing.subject_marks if mark.id is not None}
    
    updated_marks = []
    for mark_data in payload.subject_marks:
        if mark_data.id in existing_marks:
            existing_mark = existing_marks[mark_data.id]
            existing_mark.mark = mark_data.mark
            existing_mark.subject_name = mark_data.subject_name
        else:
            new_mark = SubjectMark(
                mark=mark_data.mark,
                subject_name=mark_data.subject_name,
                student_id=existing.id,
                teacher_id=existing.teacher_id
            )
            db.add(new_mark)
            updated_marks.append(new_mark)
    
    db.commit()
    db.refresh(existing)
    return ResponseModel(data=StudentSchema.from_orm(existing), message="Student updated successfully")


async def get_all_student(db: Session = Depends(get_db), search: str = None, is_pagination: bool = True, limit: int = 10, skip: int = 0):
    query = db.query(Student).options(joinedload(Student.subject_marks))
    if search:
        query = query.filter(
            Student.student_name.contains(search)
        )
    if is_pagination:
        query = query.limit(limit).offset(skip)  
    students = query.all()
    total = query.count()
    return ResponseModel(data={
        "students": [StudentSchema.from_orm(student) for student in students],
        "total": total
    }, message="Students fetched successfully")


async def get_student_by_id(student_id: int, db: Session = Depends(get_db)):
    student = (
        db.query(Student)
        .options(joinedload(Student.subject_marks))
        .filter(Student.id == student_id)
        .first()
    )
    if not student:
        return ErrorResponseModel(error="Student not found")
    return ResponseModel(data=StudentSchema.from_orm(student), message="Student fetched successfully")


async def delete_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        return ErrorResponseModel(error="Student not found")
    db.delete(student)
    db.commit()
    return ResponseModel(data={"message": "Student deleted successfully"}, message="Student deleted successfully")


async def add_mark(payload: MarksCreateSchema, db: Session = Depends(get_db)):
    mark = db.query(SubjectMark).filter(SubjectMark.student_id == payload.student_id).first()
    if mark:
        mark.mark = payload.mark
        mark.subject_name = payload.subject_name
        mark.teacher_id = payload.teacher_id
        db.commit()
        db.refresh(mark)
        return ResponseModel(data=MarksSchema.from_orm(mark), message="Mark updated successfully")

    new_mark = SubjectMark(**payload.dict())
    db.add(new_mark)
    db.commit()
    db.refresh(new_mark)
    return ResponseModel(data=MarksSchema.from_orm(new_mark), message="Mark created successfully")

async def update_mark(mark_id: int, payload: MarksUpdateSchema, db: Session = Depends(get_db)):
    mark = db.query(SubjectMark).filter(SubjectMark.id == mark_id).first()
    if not mark:
        return ErrorResponseModel(error="Mark not found")
    mark.mark = payload.mark
    mark.subject_name = payload.subject_name
    mark.teacher_id = payload.teacher_id
    db.commit()
    db.refresh(mark)
    return ResponseModel(data=MarksSchema.from_orm(mark), message="Mark updated successfully")


async def delete_mark_by_id(student_id: int, mark_id: int, db: Session = Depends(get_db)):
    mark = db.query(SubjectMark).filter(SubjectMark.id == mark_id, SubjectMark.student_id == student_id).first()
    if not mark:
        return ErrorResponseModel(error="Mark not found")
    db.delete(mark)
    db.commit()
    return ResponseModel(data={"message": "Mark deleted successfully"}, message="Mark deleted successfully")
