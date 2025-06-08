from fastapi import APIRouter, Depends
from src.app.auth.service import register_user, login_user
from src.app.auth.schema import RegisterSchema, LoginSchema
from src.database.db_config import get_db
from sqlalchemy.orm import Session

router = APIRouter(tags=["Auth"])


@router.post("/register")
async def register(payload: RegisterSchema, db: Session = Depends(get_db)):
    response = await register_user(payload, db)
    return response

@router.post("/login")
async def login(payload: LoginSchema, db: Session = Depends(get_db)):
    response = await login_user(payload, db)
    return response

