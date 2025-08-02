from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from models.book_model import Book
from schema.book_schema import BookResponse, BookCreate, BookUpdate
from models.database import get_db

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
    search_criteria = []
    
    if isbn:
        search_criteria.append(f"ISBN '{isbn}'")
    if title:
        search_criteria.append(f"Titel '{title}'")
    if author:
        search_criteria.append(f"Autor '{author}'")
    if category:
        search_criteria.append(f"Kategorie '{category}'")
    
    query = apply_book_filters(query, isbn, title, author, category)
    books = query.all()
    
    # Wenn Suchkriterien angegeben wurden, aber keine Bücher gefunden wurden
    if search_criteria and not books:
        criteria_text = ", ".join(search_criteria)
        raise HTTPException(
            status_code=404, 
            detail=f"Kein Buch mit {criteria_text} gefunden."
        )
    
    return books

@router.get("/{isbn}", response_model=BookResponse)
def get_book(isbn: str, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.isbn == isbn).first()
    if not book:
        raise HTTPException(
            status_code=404,
            detail=f"Book with ISBN {isbn} not found."
        )
    return book

@router.post("/", response_model=BookResponse)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    # Check if ISBN already exists
    existing_book = db.query(Book).filter(Book.isbn == book.isbn).first()
    if existing_book:
        raise HTTPException(status_code=400, detail=f"Book with ISBN '{book.isbn}' already exists")
    
    db_book = Book(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

@router.put("/{isbn}", response_model=BookResponse)
def update_book(isbn: str, book: BookUpdate, db: Session = Depends(get_db)):
    db_book = db.query(Book).filter(Book.isbn == isbn).first()
    if not db_book:
        raise HTTPException(status_code=404, detail=f"Book with ISBN {isbn} not found")
    
    # Check ISBN uniqueness if being updated
    if book.isbn and book.isbn != db_book.isbn:
        existing_book = db.query(Book).filter(Book.isbn == book.isbn).first()
        if existing_book:
            raise HTTPException(status_code=400, detail=f"Book with ISBN '{book.isbn}' already exists")
    
    for key, value in book.dict(exclude_unset=True).items():
        setattr(db_book, key, value)
    
    db.commit()
    db.refresh(db_book)
    return db_book

@router.delete("/{isbn}")
def delete_book(isbn: str, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.isbn == isbn).first()
    if not book:
        raise HTTPException(
            status_code=404,
            detail=f"Book with ISBN {isbn} not found."
        )
    db.delete(book)
    db.commit()
    return {"message": f"Book with ISBN {isbn} deleted."}