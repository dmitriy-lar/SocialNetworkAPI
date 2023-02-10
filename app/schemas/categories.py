from pydantic import BaseModel


class CategoryRequestScheme(BaseModel):
    title: str


class CategoryResponseScheme(BaseModel):
    id: int
    title: str

    class Config:
        orm_mode = True
