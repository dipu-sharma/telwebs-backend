
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt
# Constants (ideally loaded from environment variables)
JWT_SECRET = "Sv/w?/T@^CN8RR$O8^I7Tss6'j76iyb"
JWT_ALGORITHM = "HS256"
JWT_EXPIRE_MINUTES = 120

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Utils
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=JWT_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
