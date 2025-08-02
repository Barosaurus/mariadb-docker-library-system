from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date
from models.user import UserStatus

class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: Optional[str] = None

class UserCreate(UserBase):
    user_number: str

class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    status: Optional[UserStatus] = None

class UserResponse(UserBase):
    id: int
    user_number: str
    registration_date: Optional[date] = None
    status: UserStatus
    
    class Config:
        from_attributes = True