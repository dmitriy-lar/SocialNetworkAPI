import sqlalchemy
from ..databases import Base


class Category(Base):
    __tablename__ = "categories"

    id = sqlalchemy.Column(
        sqlalchemy.Integer, autoincrement=True, primary_key=True, index=True
    )
    title = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=False)

    def __str__(self):
        return self.title
