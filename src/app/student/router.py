from fastapi import APIRouter, Depends
from src.app.student.service import (
    create_or_update_student,
    get_all_student,
    get_student_by_id,
    update_student,
    delete_student,
    delete_mark_by_id,
)
from src.app.student.schema import StudentCreateSchema, StudentUpdateSchema, StudentFilterSchema
from src.app.auth.service import get_current_user
from src.database.db_config import get_db
from sqlalchemy.orm import Session

router = APIRouter(tags=["Student"])


@router.post("/add-student")
async def studend_add(
    payload: StudentCreateSchema,
    db: Session = Depends(get_db),
    curent_user: str = Depends(get_current_user),
):
    response = await create_or_update_student(payload, db)
    return response


@router.get("/all-student")
async def all_student(
    filter: StudentFilterSchema = Depends(),
    is_pagination: bool = True,
    db: Session = Depends(get_db), curent_user: str = Depends(get_current_user)
):
    response = await get_all_student(db, **filter.dict(), is_pagination=is_pagination)
    return response


@router.get("/get-student")
async def get_student(
    student_id: int,
    db: Session = Depends(get_db),
    curent_user: str = Depends(get_current_user),
):
    response = await get_student_by_id(student_id, db)
    return response


@router.put("/update-student")
async def student_update(
    student_id: int,
    payload: StudentUpdateSchema,
    db: Session = Depends(get_db),
    curent_user: str = Depends(get_current_user),
):
    response = await update_student(student_id, payload, db)
    return response


@router.delete("/delete-student")
async def student_delete(
    student_id: int,
    db: Session = Depends(get_db),
    curent_user: str = Depends(get_current_user),
):
    response = await delete_student(student_id, db)
    return response


@router.delete("/delete-mark")
async def delete_mark(
    student_id: int,
    mark_id: int,
    db: Session = Depends(get_db),
    curent_user: str = Depends(get_current_user),
):
    response = await delete_mark_by_id(student_id, mark_id, db)
    return response