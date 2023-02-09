from ..databases import AsyncSession
from ..dependencies import get_db
from fastapi import APIRouter, Depends
# from ..schemas.users import User
# from ..models.users import User
from sqlalchemy import select

router = APIRouter()


# @router.post('/users')
# async def create_user(username: str, db: AsyncSession = Depends(get_db)):
#     user = User(username=username)
#     db.add(user)
#     await db.commit()
#     await db.refresh(user)
#     return user
#
#
# @router.get('/users')
# async def list_users(db: AsyncSession = Depends(get_db)):
#     users = await db.execute(select(User))
#     return users.scalars().all()
