from pydantic import BaseModel
from typing import Optional

class BookBase(BaseModel):
    isbn: str
    title: str
    author: str
    category: Optional[str] = None
    publication_year: Optional[int] = None
    available_copies: Optional[int] = None
    total_copies: Optional[int] = None

class BookCreate(BookBase):
    pass

class BookUpdate(BaseModel):
    isbn: Optional[str] = None
    title: Optional[str] = None
    author: Optional[str] = None
    category: Optional[str] = None
    publication_year: Optional[int] = None
    available_copies: Optional[int] = None
    total_copies: Optional[int] = None

class BookResponse(BookBase):
    id: int

    class Config:
        from_attributes = True
