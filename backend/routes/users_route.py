from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from models.database import get_db
from models.user_model import User, UserStatus
from schemas.user_schema import UserCreate, UserUpdate, UserResponse
from typing import List

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

@router.get("/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
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
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(db_user)
    db.commit()
    return {"message": "User deleted successfully"}