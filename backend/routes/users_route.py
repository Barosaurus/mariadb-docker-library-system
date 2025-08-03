from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from models.user_model import User
from models.loan_model import Loan
from schema.user_schema import UserResponse, UserCreate, UserUpdate
from models.database import get_db

router = APIRouter()

@router.get("/", response_model=List[UserResponse])
def get_users(
    email: str = Query(None),
    name: str = Query(None),
    status: str = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(User)
    search_criteria = []
    
    if email:
        query = query.filter(User.email == email)
        search_criteria.append(f"E-Mail '{email}'")
    if name:
        query = query.filter(
            (User.first_name.like(f"%{name}%")) | 
            (User.last_name.like(f"%{name}%"))
        )
        search_criteria.append(f"Name '{name}'")
    if status:
        query = query.filter(User.status == status)
        search_criteria.append(f"Status '{status}'")
    
    users = query.all()
    
    # Meldung, wenn keine Benutzer gefunden wurden
    if search_criteria and not users:
        criteria_text = ", ".join(search_criteria)
        raise HTTPException(
            status_code=404, 
            detail=f"Kein Benutzer mit {criteria_text} gefunden."
        )
    
    return users

@router.get("/{user_number}", response_model=UserResponse)
def get_user(user_number: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.user_number == user_number).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"User with user_number {user_number} not found.")
    return user

@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # Überprüfen, ob die E-Mail oder die Benutzer-Nummer bereits existiert
    existing_user = db.query(User).filter(
        (User.email == user.email) | (User.user_number == user.user_number)
    ).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User with this user number already exists")
    
    db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.put("/{user_number}", response_model=UserResponse)
def update_user(user_number: str, user: UserUpdate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.user_number == user_number).first()
    if not db_user:
        raise HTTPException(status_code=404, detail=f"User with user_number {user_number} not found")
    
    if user.email and user.email != db_user.email:
        existing_user = db.query(User).filter(User.email == user.email).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="User with this email already exists")
    
    for key, value in user.dict(exclude_unset=True).items():
        setattr(db_user, key, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user

@router.delete("/{user_number}")
def delete_user(user_number: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.user_number == user_number).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"User with user_number {user_number} not found.")
    active_loans = db.query(Loan).filter(Loan.user_number == user_number).all()
    if active_loans:
        raise HTTPException(
            status_code=400,
            detail=f"User with user_number {user_number} cannot be deleted: active loans exist."
        )
    db.delete(user)
    db.commit()
    return {"message": f"User with user_number {user_number} deleted."}