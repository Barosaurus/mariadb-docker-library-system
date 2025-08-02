from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional
from models.user_model import UserStatus

class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: Optional[str] = None

class UserCreate(UserBase):
    user_number: str

class UserUpdate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    status: UserStatus

class UserResponse(UserBase):
    user_number: str
    registration_date: Optional[date] = None
    status: UserStatus
    class Config:
        from_attributes = True