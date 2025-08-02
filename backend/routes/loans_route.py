from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from models.loan_model import Loan
from models.book_model import Book
from models.user_model import User
from models.database import get_db
from schema.loan_schema import LoanCreate, LoanUpdate, LoanResponse
from typing import List
from datetime import date, timedelta

router = APIRouter()

@router.get("/", response_model=List[LoanResponse])
def get_loans(
    user_number: str = Query(None, description="Filter by user number"),
    book_isbn: str = Query(None, description="Filter by book ISBN"),
    status: str = Query(None, description="Filter by status: active, returned, overdue"),
    db: Session = Depends(get_db)
):
    query = db.query(Loan)
    if user_number:
        query = query.filter(Loan.user_number == user_number)
    if book_isbn:
        query = query.filter(Loan.book_isbn == book_isbn)
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
        loan_dict["id"] = loan.id
        result.append(LoanResponse(**loan_dict))
    return result

@router.get("/{loan_id}", response_model=LoanResponse)
def get_loan(loan_id: int, db: Session = Depends(get_db)):
    loan = db.query(Loan).filter(Loan.id == loan_id).first()
    if not loan:
        raise HTTPException(
            status_code=404,
            detail=f"Loan with id {loan_id} not found."
        )
    return loan

@router.post("/", response_model=LoanResponse)
def create_loan(loan: LoanCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.user_number == loan.user_number).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"User with user_number {loan.user_number} not found.")
    book = db.query(Book).filter(Book.isbn == loan.book_isbn).first()
    if not book:
        raise HTTPException(status_code=404, detail=f"Book with ISBN {loan.book_isbn} not found.")
    # NEU: Prüfe auf verfügbare Exemplare
    if book.available_copies < 1:
        raise HTTPException(status_code=400, detail="No available copies for this book.")
    # Loan anlegen & Buchbestand reduzieren
    new_loan = Loan(
        user_number=loan.user_number,
        book_isbn=loan.book_isbn,
        loan_date=date.today(),
        due_date=loan.due_date,
        return_date=None
    )
    book.available_copies -= 1
    db.add(new_loan)
    db.commit()
    db.refresh(new_loan)
    
    # Ergänze die zusätzlichen Felder für die Response
    loan_dict = new_loan.__dict__.copy()
    loan_dict["book_title"] = book.title
    loan_dict["user_name"] = f"{user.first_name} {user.last_name}"
    return LoanResponse(**loan_dict)

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
    book = db.query(Book).filter(Book.isbn == db_loan.book_isbn).first()
    book.available_copies += 1
    
    db.commit()
    db.refresh(db_loan)
    
    # Ergänze die zusätzlichen Felder für die Response
    user = db.query(User).filter(User.user_number == db_loan.user_number).first()
    loan_dict = db_loan.__dict__.copy()
    loan_dict["book_title"] = book.title if book else ""
    loan_dict["user_name"] = f"{user.first_name} {user.last_name}" if user else ""
    loan_dict["id"] = db_loan.id
    return LoanResponse(**loan_dict)

@router.put("/{loan_id}", response_model=LoanResponse)
def update_loan(loan_id: int, loan: LoanUpdate, db: Session = Depends(get_db)):
    db_loan = db.query(Loan).filter(Loan.id == loan_id).first()
    if not db_loan:
        raise HTTPException(status_code=404, detail="Loan not found")
    
    for key, value in loan.dict(exclude_unset=True).items():
        setattr(db_loan, key, value)
    
    db.commit()
    db.refresh(db_loan)
    
    # Ergänze die zusätzlichen Felder für die Response
    book = db.query(Book).filter(Book.isbn == db_loan.book_isbn).first()
    user = db.query(User).filter(User.user_number == db_loan.user_number).first()
    loan_dict = db_loan.__dict__.copy()
    loan_dict["book_title"] = book.title if book else ""
    loan_dict["user_name"] = f"{user.first_name} {user.last_name}" if user else ""
    loan_dict["id"] = db_loan.id
    return LoanResponse(**loan_dict)

@router.delete("/{loan_id}")
def delete_loan(loan_id: int, db: Session = Depends(get_db)):
    loan = db.query(Loan).filter(Loan.id == loan_id).first()
    if not loan:
        raise HTTPException(
            status_code=404,
            detail=f"Loan with id {loan_id} not found."
        )
    db.delete(loan)
    db.commit()
    return {"message": f"Loan {loan_id} deleted."}