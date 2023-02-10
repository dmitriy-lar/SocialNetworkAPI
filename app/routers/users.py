from ..tags import Tags
from ..models.users import User
from ..dependencies import get_db
from ..utils import get_current_user
from ..databases import AsyncSession
from ..schemas.users import UserScheme, UserInDBScheme
from ..utils import hashed_password, verify_password, create_access_token
from ..Responses.users import (
    register_responses,
    login_responses,
    current_user_responses,
)
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from fastapi import status
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from ..settings import config_env

router = APIRouter(prefix="/api/users")


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    tags=[Tags.users.value],
    summary="Register user",
    description="""**Register a new user**""",
    responses={
        201: register_responses.response["201"],
        400: register_responses.response["400"],
    },
)
async def create_user(
    user_scheme: UserInDBScheme, db: AsyncSession = Depends(get_db)
) -> dict:
    user = await db.execute(select(User).where(User.email == user_scheme.email))
    if user.first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists",
        )

    user = User(email=user_scheme.email, password=hashed_password(user_scheme.password))
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return {
        "user": {"id": user.id, "email": user.email},
        "message": "Successfully registered",
    }


@router.post(
    "/login",
    summary="Login User",
    description="""**Login user**""",
    tags=[Tags.users],
    status_code=status.HTTP_200_OK,
    responses={
        200: login_responses.response["200"],
        400: login_responses.response["400"],
    },
)
async def login_user(
    db: AsyncSession = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
) -> dict:
    credentials_exception = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid email or password"
    )

    user = await db.execute(select(User).where(User.email == form_data.username))

    try:
        user = user.scalar_one()
    except NoResultFound:
        user = None

    if user is None:
        raise credentials_exception

    hashed_password = user.password

    if not verify_password(form_data.password, hashed_password):
        raise credentials_exception

    access_token = create_access_token(user.email)

    return {"access_token": access_token}


@router.get(
    "/me",
    response_model=UserScheme,
    status_code=status.HTTP_200_OK,
    summary="Get current user",
    description="""**Get current user**""",
    tags=[Tags.users],
    responses={
        200: current_user_responses.response["200"],
        400: current_user_responses.response["400"],
    },
)
async def current_user(user: User = Depends(get_current_user)):
    return user


@router.post(
    "/create-admin",
    summary="Create an admin user",
    description="""**Create an admin user**""",
    tags=[Tags.users],
    status_code=status.HTTP_201_CREATED,
)
async def create_admin_user(
    user_scheme: UserInDBScheme, key: str, db: AsyncSession = Depends(get_db)
) -> dict:
    if key != config_env["KEY"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid key"
        )

    user = await db.execute(select(User).where(User.email == user_scheme.email))
    if user.first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Admin user with this email already exists",
        )

    user = User(
        email=user_scheme.email,
        password=hashed_password(user_scheme.password),
        is_admin=True,
    )

    db.add(user)
    await db.commit()
    await db.refresh(user)

    return {
        "user": {"id": user.id, "email": user.email},
        "message": "Admin user created successfully",
    }


@router.get("/list", response_model=list[UserScheme])
async def users_list(db: AsyncSession = Depends(get_db)):
    users = await db.execute(select(User))
    return users.scalars().all()
