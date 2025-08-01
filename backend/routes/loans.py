from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from models import Loan, Book
from models.database import get_db
from schemas import LoanResponse, LoanCreate, LoanUpdate
from typing import List
from datetime import date, timedelta

router = APIRouter()

@router.get("/", response_model=List[LoanResponse])
def get_loans(
    user_id: int = Query(None),
    book_id: int = Query(None),
    status: str = Query(None),  # "active" oder "returned"
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
    return query.all()

@router.post("/", response_model=LoanResponse)
def create_loan(loan: LoanCreate, db: Session = Depends(get_db)):
    # Überprüfe, ob das Buch verfügbar ist
    book = db.query(Book).filter(Book.id == loan.book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    if book.available_copies <= 0:
        raise HTTPException(status_code=400, detail="Book is not available")
    
    # Erstelle die Ausleihe
    db_loan = Loan(
        **loan.dict(),
        loan_date=date.today(),
        due_date=date.today() + timedelta(days=14)  # 2 Wochen Ausleihfrist
    )
    
    # Reduziere die verfügbaren Kopien
    book.available_copies -= 1
    
    db.add(db_loan)
    db.commit()
    db.refresh(db_loan)
    return db_loan

@router.put("/{loan_id}/return", response_model=LoanResponse)
def return_book(loan_id: int, db: Session = Depends(get_db)):
    # Finde die Ausleihe
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
