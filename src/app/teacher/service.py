from src.modals.modal import Teacher
from src.database.db_config import get_db
from sqlalchemy.orm import Session
from src.app.teacher.schema import CreateTeacherSchema, TeacherSchema, UpdateTeacherSchema
from fastapi import Depends, status
from sqlalchemy.orm import joinedload

async def create_or_update_teacher(
    payload: CreateTeacherSchema, db: Session = Depends(get_db)
):
    existing = (
        db.query(Teacher)
        .options(joinedload(Teacher.subject_marks))
        .filter(
            Teacher.teacher_name == payload.teacher_name,
            Teacher.subject == payload.subject,
        )
        .first()
    )

    if existing:
        existing.subject_marks = payload.subject_marks
        db.commit()
        db.refresh(existing)
        return TeacherSchema.from_orm(existing), "Teacher mark updated successfully"

    new_teacher = Teacher(**payload.dict())
    db.add(new_teacher)
    db.commit()
    db.refresh(new_teacher)
    return TeacherSchema.from_orm(new_teacher), "Teacher created successfully"


async def update_teacher(
    payload: UpdateTeacherSchema, db: Session = Depends(get_db)
):
    existing = (
        db.query(Teacher)
        .options(joinedload(Teacher.subject_marks))
        .filter(
            Teacher.teacher_name == payload.teacher_name,
            Teacher.subject == payload.subject,
        )
        .first()
    )

    if not existing:
        return {"message": "Teacher not found"}, status.HTTP_404_NOT_FOUND

    existing.subject_marks = payload.subject_marks
    db.commit()
    db.refresh(existing)
    return TeacherSchema.from_orm(existing), "Teacher mark updated successfully"


async def get_teacher_by_id(teacher_id: int, db: Session = Depends(get_db)):
    teacher = (
        db.query(Teacher)
        .options(joinedload(Teacher.subject_marks))
        .filter(Teacher.id == teacher_id)
        .first()
    )
    if not teacher:
        return {"message": "Teacher not found"}, status.HTTP_404_NOT_FOUND
    return TeacherSchema.from_orm(teacher)


async def delete_teacher(teacher_id: int, db: Session = Depends(get_db)):
    teacher = db.query(Teacher).filter(Teacher.id == teacher_id).first()
    if not teacher:
        return {"message": "Teacher not found"}, status.HTTP_404_NOT_FOUND
    db.delete(teacher)
    db.commit()
    return {"message": "Teacher deleted successfully"}, status.HTTP_200_OK


