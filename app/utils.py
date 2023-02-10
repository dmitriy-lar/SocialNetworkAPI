from datetime import datetime, timedelta
from typing import Union, Any
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from .databases import AsyncSession
from .models.users import User
from .schemas.users import UserScheme
from .settings import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM
from jose import jwt, JWTError
from passlib.context import CryptContext
from .settings import config_env
from .dependencies import get_db

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
JWT_SECRET_KEY = config_env.get("JWT_SECRET_KEY")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/users/login", scheme_name="JWT")


def hashed_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)


def create_access_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, ALGORITHM)
    return encoded_jwt


async def get_current_user(
        token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)
) -> UserScheme:
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials or token is expired",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = await db.execute(select(User).where(User.email == username))
    try:
        user = user.scalar_one()
    except NoResultFound:
        user = None

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user


async def is_admin_user(db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)) -> bool:
    if not user.is_admin:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='You do not have enough permissions')
    return True
