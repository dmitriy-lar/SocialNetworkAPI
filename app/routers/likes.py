from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import except_
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm.attributes import register_attribute
from sqlalchemy.sql import select
from app.models.likes import Like
from app.models.users import User
from app.tags import Tags
from ..databases import AsyncSession
from ..dependencies import get_db
from ..models.posts import Post
from ..utils import get_current_user


router = APIRouter(prefix="/api/likes")


@router.post(
    "/add/{post_id}",
    summary="Add like to post",
    description="""**Add like to post**""",
    tags=[Tags.likes],
    status_code=status.HTTP_200_OK,
    # TODO: responses
)
async def add_like(
    post_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> dict:
    posts_query = await db.execute(select(Post).where(Post.id == post_id))

    try:
        post = posts_query.scalar_one()
    except NoResultFound:
        post = None

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post was not found"
        )

    if post.user_id == user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Owner of the post cannot like it",
        )

    post_like_query = await db.execute(select(Like).where(Like.post_id == post_id))

    try:
        posts_likes = post_like_query.scalar_one()
    except NoResultFound:
        posts_likes = None

    if posts_likes is None:
        like = Like(post_id=post_id, user_id=user.id, liked=True)

        db.add(like)
        await db.commit()
        return {"message": "Post was successfully liked"}

    else:
        if posts_likes.liked:
            posts_likes.liked = False

            await db.commit()
            return {"message": "Post was successfully unliked"}
        else:
            posts_likes.liked = True
            await db.commit()
            return {"message": "Post was successfully liked"}
