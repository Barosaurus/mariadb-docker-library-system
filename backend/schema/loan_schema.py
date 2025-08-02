from pydantic import BaseModel
from typing import Optional
from datetime import date


class LoanBase(BaseModel):
    user_number: str
    book_isbn: str
    due_date: date

class LoanCreate(LoanBase):
    pass

class LoanUpdate(BaseModel):
    return_date: Optional[date] = None
    due_date: Optional[date] = None

class LoanResponse(LoanBase):
    id: int
    user_number: str
    book_isbn: str
    due_date: date
    loan_date: date
    return_date: Optional[date] = None
    book_title: str
    user_name: str
    class Config:
        from_attributes = True

def some_function(loan_dict):
    return LoanResponse(**loan_dict)