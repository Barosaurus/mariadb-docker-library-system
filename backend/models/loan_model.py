from sqlalchemy import Column, Integer, ForeignKey, Date
from sqlalchemy.orm import relationship
from models.database import Base

class Loan(Base):
    __tablename__ = "loans"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    loan_date = Column(Date, nullable=False)
    return_date = Column(Date)
    due_date = Column(Date, nullable=False)
    
    user = relationship("User", backref="loans")
    book = relationship("Book", backref="loans")
