from ..databases import AsyncSession
from ..dependencies import get_db
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from ..schemas.users import UserScheme, UserInDBScheme
from fastapi import status
from ..models.users import User
from app.Responses.users.register_responses import response
from ..utils import hashed_password
from ..tags import Tags

router = APIRouter(prefix='/api/users')


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    responses={201: response["201"], 400: response["400"]},
    tags=[Tags.users.value],
    summary="Register user",
    description="""**Register a new user**""",
)
async def create_user(user_scheme: UserInDBScheme, db: AsyncSession = Depends(get_db)):
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


@router.get("/list", response_model=list[UserScheme])
async def users_list(db: AsyncSession = Depends(get_db)):
    users = await db.execute(select(User))
    return users.scalars().all()
