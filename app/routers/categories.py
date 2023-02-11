from typing import Sequence
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from ..tags import Tags
from fastapi import status
from fastapi import APIRouter, Depends, HTTPException
from ..schemas.categories import CategoryRequestScheme, CategoryResponseScheme
from ..Responses.categories import (
    categories_create,
    categories_list,
    category_one,
    categories_delete,
)
from ..databases import AsyncSession
from ..dependencies import get_db
from ..models.categories import Category
from ..utils import is_admin_user, get_current_user
from ..models.users import User

router = APIRouter(prefix="/api/categories")


@router.post(
    "/create",
    summary="Create category",
    description="""**Create category**""",
    tags=[Tags.categories],
    responses={
        201: categories_create.response["201"],
        400: categories_create.response["400"],
        401: categories_create.response["401"],
    },
    response_model=CategoryResponseScheme,
    status_code=status.HTTP_201_CREATED,
)
async def category_create(
    category_item: CategoryRequestScheme,
    db: AsyncSession = Depends(get_db),
    is_admin: bool = Depends(is_admin_user),
) -> CategoryResponseScheme:
    category_query = await db.execute(
        select(Category).where(Category.title == category_item.title)
    )
    category = category_query.first()

    if category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Category already exists"
        )

    category = Category(**category_item.dict())
    db.add(category)
    await db.commit()
    await db.refresh(category)

    return category


@router.get(
    "/list",
    summary="List of categories",
    description="""**List of categories**""",
    tags=[Tags.categories],
    status_code=status.HTTP_200_OK,
    response_model=list[CategoryResponseScheme],
    responses={
        200: categories_list.response["200"],
        401: categories_list.response["401"],
    },
)
async def list_of_categories(
    db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)
) -> Sequence[Category]:
    categories_query = await db.execute(select(Category))
    return categories_query.scalars().all()


@router.get(
    "/{category_id}",
    summary="Get category",
    description="""**Get category by _id_**""",
    tags=[Tags.categories],
    status_code=status.HTTP_200_OK,
    response_model=CategoryResponseScheme,
    responses={
        200: category_one.response["200"],
        401: category_one.response["401"],
        404: category_one.response["404"],
    },
)
async def get_category(
    category_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> CategoryResponseScheme:
    category_query = await db.execute(
        select(Category).where(Category.id == category_id)
    )

    try:
        category = category_query.scalar_one()
    except NoResultFound:
        category = None

    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Category was not found"
        )

    return category


@router.put(
    "/{category_id}/update",
    summary="Update category",
    description="""**Update category by _id_**""",
    tags=[Tags.categories],
    response_model=CategoryResponseScheme,
    status_code=status.HTTP_201_CREATED,
    responses={
        201: category_one.response["201"],
        401: category_one.response["401"],
        404: category_one.response["404"],
    },
)
async def update_category(
    category_id: int,
    category_scheme: CategoryRequestScheme,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
    is_admin: bool = Depends(is_admin_user),
) -> CategoryResponseScheme:
    category_query = await db.execute(
        select(Category).where(Category.id == category_id)
    )

    try:
        category = category_query.scalar_one()
    except NoResultFound:
        category = None

    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Category was not found"
        )
    category.title = category_scheme.title
    db.add(category)
    await db.commit()
    await db.refresh(category)

    return category


@router.delete(
    "/{category_id}/delete}",
    summary="Delete category",
    description="""**Delete category by _id_**""",
    tags=[Tags.categories],
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        401: categories_delete.response["401"],
        404: categories_delete.response["404"],
    },
)
async def delete_category(
    category_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
    is_admin: bool = Depends(is_admin_user),
) -> None:
    category_query = await db.execute(
        select(Category).where(Category.id == category_id)
    )

    try:
        category = category_query.scalar_one()
    except NoResultFound:
        category = None

    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Category was not found"
        )

    await db.delete(category)
    await db.commit()
