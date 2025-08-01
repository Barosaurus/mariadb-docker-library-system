from pydantic import BaseModel
from typing import Optional
from datetime import date

class LoanBase(BaseModel):
    user_id: int
    book_id: int
    due_date: date

class LoanCreate(LoanBase):
    pass

class LoanUpdate(BaseModel):
    return_date: Optional[date] = None
    due_date: Optional[date] = None

class LoanResponse(LoanBase):
    id: int
    loan_date: date
    return_date: Optional[date] = None

    class Config:
        from_attributes = True
