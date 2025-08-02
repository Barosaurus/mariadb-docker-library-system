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

class BookUpdate(BaseModel):
    isbn: str
    title: str
    author: str
    category: str
    publication_year: int
    available_copies: int
    total_copies: int

class BookResponse(BookBase):
    class Config:
        from_attributes = True