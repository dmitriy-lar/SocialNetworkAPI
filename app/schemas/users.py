from pydantic import BaseModel, EmailStr


class UserScheme(BaseModel):
    email: EmailStr

    class Config:
        orm_mode = True


class UserInDBScheme(UserScheme):
    password: str
