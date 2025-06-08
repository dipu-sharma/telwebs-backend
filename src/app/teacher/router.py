from fastapi import APIRouter, Depends
from src.app.teacher.service import (
    create_or_update_teacher,
    get_teacher_by_id,
    update_teacher,
    delete_teacher,
)
from src.app.teacher.schema import CreateTeacherSchema, UpdateTeacherSchema
from src.app.auth.service import get_current_user
from src.database.db_config import get_db
from sqlalchemy.orm import Session

router = APIRouter(tags=["Teacher"])

@router.post("/add-teacher")
async def teacher_add(
    payload: CreateTeacherSchema,
    db: Session = Depends(get_db),
    curent_user: str = Depends(get_current_user),
):
    return await create_or_update_teacher(payload, db)

@router.get("/get-teacher")
async def get_teacher_by_id(
    teacher_id: int,
    db: Session = Depends(get_db),
    curent_user: str = Depends(get_current_user),
):
    return await get_teacher_by_id(teacher_id, db)

@router.put("/update-teacher")
async def update_teacher(
    teacher_id: int,
    payload: UpdateTeacherSchema,
    db: Session = Depends(get_db),
    curent_user: str = Depends(get_current_user),
):
    return await update_teacher(teacher_id, payload, db)

@router.delete("/delete-teacher")
async def delete_teacher(
    teacher_id: int,
    db: Session = Depends(get_db),
    curent_user: str = Depends(get_current_user),
):
    return await delete_teacher(teacher_id, db)
