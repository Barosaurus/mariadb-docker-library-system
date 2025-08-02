from pydantic import BaseModel
from typing import Optional

class BookBase(BaseModel):
    isbn: str
    title: str
    author: str
    category: Optional[str] = None
    publication_year: Optional[int] = None
    available_copies: Optional[int] = 1
    total_copies: Optional[int] = 1

class BookCreate(BookBase):
    isbn: str
    title: str
    author: str
    category: str
    publication_year: int
    available_copies: int
    total_copies: int

    @classmethod
    def validate(cls, value):
        if value['total_copies'] < value['available_copies']:
            raise ValueError('total_copies darf nicht kleiner als available_copies sein!')
        return value

class BookUpdate(BaseModel):
    isbn: str
    title: str
    author: str
    category: str
    publication_year: int
    available_copies: int
    total_copies: int

    @classmethod
    def validate(cls, value):
        if value['total_copies'] < value['available_copies']:
            raise ValueError('total_copies darf nicht kleiner als available_copies sein!')
        return value

class BookResponse(BookBase):
    class Config:
        from_attributes = True