from typing import Sequence
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from ..tags import Tags
from fastapi import status
from fastapi import APIRouter, Depends, HTTPException
from ..databases import AsyncSession
from ..dependencies import get_db
from ..models.posts import Post
from ..utils import get_current_user
from ..models.users import User
from ..models.categories import Category
from ..schemas.posts import PostRequestScheme, PostResponseScheme
from ..Responses.posts import post_create, post_list, post_one

router = APIRouter(prefix="/api/posts")


@router.post(
    "/create",
    summary="Create post",
    description="""**Create post**""",
    tags=[Tags.posts],
    status_code=status.HTTP_201_CREATED,
    response_model=PostResponseScheme,
    responses={
        201: post_create.response["201"],
        401: post_create.response["401"],
        404: post_create.response["404"],
    },
)
async def create_post(
    post_scheme: PostRequestScheme,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    category = await db.execute(
        select(Category).where(Category.id == post_scheme.category_id)
    )

    try:
        category = category.scalar_one()
    except NoResultFound:
        category = None

    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No such category with id {post_scheme.category_id}",
        )

    post = Post(**post_scheme.dict(), user_id=user.id)
    db.add(post)
    await db.commit()
    await db.refresh(post)
    return post


@router.get(
    "/list",
    summary="List of posts",
    description="""**List of posts**""",
    tags=[Tags.posts],
    status_code=status.HTTP_200_OK,
    response_model=list[PostResponseScheme],
    responses={200: post_list.response["200"], 401: post_list.response["401"]},
)
async def list_of_posts(
    db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)
) -> Sequence[Post]:
    posts_query = await db.execute(select(Post))

    return posts_query.scalars().all()


@router.get(
    "/me",
    summary="List of posts of current user",
    description="""**List of post of current user**""",
    tags=[Tags.posts],
    status_code=status.HTTP_200_OK,
    response_model=list[PostResponseScheme],
)
async def current_user_posts(
    db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)
) -> Sequence[Post]:
    posts_query = await db.execute(select(Post).where(Post.user_id == user.id))

    try:
        posts = posts_query.scalars().all()
    except NoResultFound:
        posts = None

    if posts is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="You do not have posts",
        )

    return posts


@router.get(
    "/{post_id}",
    summary="Get post",
    description="""**Get post by _id_**""",
    tags=[Tags.posts],
    status_code=status.HTTP_200_OK,
    response_model=PostResponseScheme,
    responses={
        200: post_one.response["200"],
        401: post_one.response["401"],
        404: post_one.response["404"],
    },
)
async def get_post(
    post_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> PostResponseScheme:
    post_query = await db.execute(select(Post).where(Post.id == post_id))

    try:
        post = post_query.scalar_one()
    except NoResultFound:
        post = None

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post was not found"
        )

    return post


@router.put(
    "/{post_id}/update",
    summary="Update post",
    description="""**Update post by _id_**""",
    tags=[Tags.posts],
    status_code=status.HTTP_200_OK,
    response_model=PostResponseScheme,
    responses={
        200: post_one.response["200"],
        401: post_one.response["401"],
        403: post_one.response["403"],
        404: post_one.response["404"],
    },
)
async def update_post(
    post_id: int,
    post_scheme: PostRequestScheme,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> PostResponseScheme:
    post_query = await db.execute(select(Post).where(Post.id == post_id))

    try:
        post = post_query.scalar_one()
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post was not found"
        )

    if post.user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not an owner of this post",
        )

    category_query = await db.execute(
        select(Category).where(Category.id == post_scheme.category_id)
    )

    try:
        category = category_query.scalar_one()
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No such category with id {post_scheme.category_id}",
        )

    post.title = post_scheme.title
    post.content = post_scheme.content
    post.category_id = post_scheme.category_id

    await db.commit()
    await db.refresh(post)

    return post


@router.delete(
    "/{post_id}/delete",
    summary="Delete post",
    description="""**Delete post by _id_**""",
    tags=[Tags.posts],
    status_code=status.HTTP_204_NO_CONTENT,
    responses={401: post_one.response["401"], 404: post_one.response["404"]},
)
async def delete_post(
    post_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> None:
    post_query = await db.execute(select(Post).where(Post.id == post_id))

    try:
        post = post_query.scalar_one()
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post was not found"
        )

    if post.user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not an owner of this post",
        )

    await db.delete(post)
    await db.commit()
