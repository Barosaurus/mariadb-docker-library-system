from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from models.loan import Loan
from models.book import Book
from models.user import User
from models.database import get_db
from schemas.loan import LoanResponse, LoanCreate, LoanUpdate
from typing import List
from datetime import date, timedelta

router = APIRouter()

@router.get("/", response_model=List[LoanResponse])
def get_loans(
    user_id: int = Query(None, description="Filter by user ID"),
    book_id: int = Query(None, description="Filter by book ID"),
    status: str = Query(None, description="Filter by status: active, returned, overdue"),
    db: Session = Depends(get_db)
):
    query = db.query(Loan)
    if user_id:
        query = query.filter(Loan.user_id == user_id)
    if book_id:
        query = query.filter(Loan.book_id == book_id)
    if status:
        if status == "active":
            query = query.filter(Loan.return_date == None)
        elif status == "returned":
            query = query.filter(Loan.return_date != None)
        elif status == "overdue":
            query = query.filter(Loan.return_date == None, Loan.due_date < date.today())
    loans = query.all()
    result = []
    for loan in loans:
        book_title = loan.book.title if loan.book else ""
        user_name = f"{loan.user.first_name} {loan.user.last_name}" if loan.user else ""
        loan_dict = loan.__dict__.copy()
        loan_dict["book_title"] = book_title
        loan_dict["user_name"] = user_name
        result.append(loan_dict)
    return result

@router.get("/{loan_id}", response_model=LoanResponse)
def get_loan(loan_id: int, db: Session = Depends(get_db)):
    loan = db.query(Loan).filter(Loan.id == loan_id).first()
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")
    book_title = loan.book.title if loan.book else ""
    user_name = f"{loan.user.first_name} {loan.user.last_name}" if loan.user else ""
    loan_dict = loan.__dict__.copy()
    loan_dict["book_title"] = book_title
    loan_dict["user_name"] = user_name
    return loan_dict

@router.post("/", response_model=LoanResponse)
def create_loan(loan: LoanCreate, db: Session = Depends(get_db)):
    # Überprüfe, ob User existiert
    user = db.query(User).filter(User.id == loan.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Überprüfe, ob Buch existiert und verfügbar ist
    book = db.query(Book).filter(Book.id == loan.book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    if book.available_copies <= 0:
        raise HTTPException(status_code=400, detail="Book is not available")
    
    # Erstelle die Ausleihe
    db_loan = Loan(
        user_id=loan.user_id,
        book_id=loan.book_id,
        loan_date=date.today(),
        due_date=loan.due_date
    )
    
    # Reduziere die verfügbaren Kopien
    book.available_copies -= 1
    
    db.add(db_loan)
    db.commit()
    db.refresh(db_loan)
    return db_loan

@router.put("/{loan_id}/return", response_model=LoanResponse)
def return_book(loan_id: int, db: Session = Depends(get_db)):
    db_loan = db.query(Loan).filter(Loan.id == loan_id).first()
    if not db_loan:
        raise HTTPException(status_code=404, detail="Loan not found")
    if db_loan.return_date:
        raise HTTPException(status_code=400, detail="Book already returned")
    
    # Setze das Rückgabedatum
    db_loan.return_date = date.today()
    
    # Erhöhe die verfügbaren Kopien
    book = db.query(Book).filter(Book.id == db_loan.book_id).first()
    book.available_copies += 1
    
    db.commit()
    db.refresh(db_loan)
    return db_loan

@router.put("/{loan_id}", response_model=LoanResponse)
def update_loan(loan_id: int, loan: LoanUpdate, db: Session = Depends(get_db)):
    db_loan = db.query(Loan).filter(Loan.id == loan_id).first()
    if not db_loan:
        raise HTTPException(status_code=404, detail="Loan not found")
    
    for key, value in loan.dict(exclude_unset=True).items():
        setattr(db_loan, key, value)
    
    db.commit()
    db.refresh(db_loan)
    return db_loan

@router.delete("/{loan_id}")
def delete_loan(loan_id: int, db: Session = Depends(get_db)):
    db_loan = db.query(Loan).filter(Loan.id == loan_id).first()
    if not db_loan:
        raise HTTPException(status_code=404, detail="Loan not found")
    
    # Wenn noch aktiv, Kopien zurückgeben
    if not db_loan.return_date:
        book = db.query(Book).filter(Book.id == db_loan.book_id).first()
        book.available_copies += 1
    
    db.delete(db_loan)
    db.commit()
    return {"message": "Loan deleted successfully"}