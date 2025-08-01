from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from models import Book
from models.database import get_db
from schemas import BookResponse

router = APIRouter()

@router.get("/", response_model=list[BookResponse])
def get_books(
    isbn: str = Query(None),
    title: str = Query(None),
    author: str = Query(None),
    category: str = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(Book)
    if isbn:
        query = query.filter(Book.isbn == isbn)
    if title:
        query = query.filter(Book.title.like(f"%{title}%"))
    if author:
        query = query.filter(Book.author.like(f"%{author}%"))
    if category:
        query = query.filter(Book.category.like(f"%{category}%"))
    return query.all()