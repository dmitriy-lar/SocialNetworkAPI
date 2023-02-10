import sqlalchemy
from ..databases import Base


class User(Base):
    __tablename__ = "users"

    id = sqlalchemy.Column(
        sqlalchemy.Integer, autoincrement=True, primary_key=True, index=True
    )
    email = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=False)
    password = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    is_admin = sqlalchemy.Column(sqlalchemy.Boolean, default=False)

    def __str__(self):
        return self.email
