from datetime import datetime
from pydantic import BaseModel


class PostScheme(BaseModel):
    title: str
    content: str


class PostRequestScheme(PostScheme):
    category_id: int


class PostResponseScheme(PostScheme):
    id: int
    category_id: int
    user_id: int
    time_created: datetime
    time_updated: datetime = None
    likes_count: int

    class Config:
        orm_mode = True
