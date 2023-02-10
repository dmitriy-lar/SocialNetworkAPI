import sqlalchemy
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..databases import Base


class Post(Base):
    __tablename__ = "posts"

    id = sqlalchemy.Column(
        sqlalchemy.Integer, autoincrement=True, primary_key=True, index=True
    )
    title = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    category_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('categories.id'))
    content = sqlalchemy.Column(sqlalchemy.Text, nullable=False)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    time_created = sqlalchemy.Column(
        sqlalchemy.DateTime(timezone=True), server_default=func.now()
    )
    time_updated = sqlalchemy.Column(
        sqlalchemy.DateTime(timezone=True), onupdate=func.now()
    )
    users = relationship("User", backref="posts")
    categories = relationship('Category', backref='posts')

    def __str__(self):
        return self.title
