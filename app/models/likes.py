import sqlalchemy
from sqlalchemy.orm import relationship
from ..databases import Base


class Like(Base):
    __tablename__ = "likes"

    id = sqlalchemy.Column(
        sqlalchemy.Integer, autoincrement=True, primary_key=True, index=True
    )
    post_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("posts.id"))
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    liked = sqlalchemy.Column(sqlalchemy.Boolean, default=False)

    posts = relationship("Post", backref="likes")
    users = relationship("User", backref="likes")
