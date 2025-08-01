from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from models.book import Book         # Direktes Import statt aus models
from models.database import get_db
from schemas.book import BookResponse  # Direktes Import statt aus schemas

router = APIRouter()

def apply_book_filters(query, isbn=None, title=None, author=None, category=None):
    if isbn:
        query = query.filter(Book.isbn == isbn)
    if title:
        query = query.filter(Book.title.like(f"%{title}%"))
    if author:
        query = query.filter(Book.author.like(f"%{author}%"))
    if category:
        query = query.filter(Book.category.like(f"%{category}%"))
    return query

@router.get("/", response_model=list[BookResponse])
def get_books(
    isbn: str = Query(None),
    title: str = Query(None),
    author: str = Query(None),
    category: str = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(Book)
    query = apply_book_filters(query, isbn, title, author, category)
    return query.all()