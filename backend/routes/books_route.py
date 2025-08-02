from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from models.book_model import Book
from models.database import get_db
from schemas.book_schema import BookCreate, BookUpdate, BookResponse
from typing import List

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

@router.get("/", response_model=List[BookResponse])
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

@router.get("/{book_id}", response_model=BookResponse)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.post("/", response_model=BookResponse)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    # Check if ISBN already exists
    existing_book = db.query(Book).filter(Book.isbn == book.isbn).first()
    if existing_book:
        raise HTTPException(status_code=400, detail="Book with this ISBN already exists")
    
    db_book = Book(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

@router.put("/{book_id}", response_model=BookResponse)
def update_book(book_id: int, book: BookUpdate, db: Session = Depends(get_db)):
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    # Check ISBN uniqueness if being updated
    if book.isbn and book.isbn != db_book.isbn:
        existing_book = db.query(Book).filter(Book.isbn == book.isbn).first()
        if existing_book:
            raise HTTPException(status_code=400, detail="Book with this ISBN already exists")
    
    for key, value in book.dict(exclude_unset=True).items():
        setattr(db_book, key, value)
    
    db.commit()
    db.refresh(db_book)
    return db_book

@router.delete("/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    db.delete(db_book)
    db.commit()
    return {"message": "Book deleted successfully"}