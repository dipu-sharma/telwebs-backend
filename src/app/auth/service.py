from fastapi import HTTPException, status, Request, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from datetime import datetime, timedelta
from passlib.context import CryptContext
from src.common.helper import JWT_SECRET, JWT_ALGORITHM
from src.modals.modal import User
from src.database.db_config import get_db
from src.app.auth.schema import UserSchema
from src.common.helper import create_access_token, verify_password, hash_password

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = HTTPBearer()



# JWT Bearer
class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        if not credentials or credentials.scheme != "Bearer":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid authentication scheme"
            )
        if not self.verify_token(credentials.credentials):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid or expired token"
            )
        return credentials.credentials

    @staticmethod
    def verify_token(token: str) -> bool:
        try:
            jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
            return True
        except JWTError:
            return False

# Current User Retrieval
async def get_current_user(token: str = Depends(oauth2_scheme)) -> int:
    try:
        payload = jwt.decode(token.credentials, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        user_id: int = payload.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user_id
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

# Registration
async def register_user(payload, db: Session = Depends(get_db)):
    hashed_pwd = hash_password(payload.password)
    user = User(email=payload.email, password=hashed_pwd, role=payload.role)
    exist = db.query(User).filter(User.email == payload.email).first()
    if exist:
        return UserSchema.from_orm(exist), 'User already exists'
    db.add(user)
    db.commit()
    db.refresh(user)
    return UserSchema.from_orm(user), 'User registered successfully'

# Login
async def login_user(payload, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.password):
        return {'message': 'Invalid email or password'}, status.HTTP_401_UNAUTHORIZED

    token_data = {"sub": str(user.id)}
    access_token = create_access_token(token_data)
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": UserSchema.from_orm(user)
    }, status.HTTP_200_OK
