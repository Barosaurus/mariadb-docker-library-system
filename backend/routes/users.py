from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from models.user import User
from models.database import get_db
from schemas.user import UserResponse, UserCreate, UserUpdate
from typing import List
from datetime import date

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
        query = query.filter(User.membership_status == status)
    return query.all()

@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(
        **user.dict()
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
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
