from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from models.user_model import User
from models.loan_model import Loan
from schemas.user_schema import UserResponse, UserCreate, UserUpdate
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
    if email:
        query = query.filter(User.email == email)
    if name:
        query = query.filter(
            (User.first_name.like(f"%{name}%")) | 
            (User.last_name.like(f"%{name}%"))
        )
    if status:
        query = query.filter(User.status == status)
    return query.all()

@router.get("/{user_number}", response_model=UserResponse)
def get_user(user_number: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.user_number == user_number).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"User with user_number {user_number} not found.")
    return user

@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # Check if email or user_number already exists
    existing_user = db.query(User).filter(
        (User.email == user.email) | (User.user_number == user.user_number)
    ).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User with this email or user number already exists")
    
    db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check email uniqueness if being updated
    if user.email and user.email != db_user.email:
        existing_user = db.query(User).filter(User.email == user.email).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="User with this email already exists")
    
    for key, value in user.dict(exclude_unset=True).items():
        setattr(db_user, key, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user

@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"User with id {user_id} not found.")
    active_loans = db.query(Loan).filter(Loan.user_id == user_id).all()
    if active_loans:
        raise HTTPException(
            status_code=400,
            detail=f"User with id {user_id} cannot be deleted: active loans exist."
        )
    db.delete(user)
    db.commit()
    return {"message": f"User {user_id} deleted."}