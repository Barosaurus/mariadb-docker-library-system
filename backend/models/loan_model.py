from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from models.database import Base

class Loan(Base):
    __tablename__ = "loans"
    id = Column(Integer, primary_key=True, index=True)
    user_number = Column(String(20), ForeignKey("users.user_number"), nullable=False)
    book_isbn = Column(String(13), ForeignKey("books.isbn"), nullable=False)
    loan_date = Column(Date, nullable=False)
    return_date = Column(Date)
    due_date = Column(Date, nullable=False)
    user = relationship("User", backref="loans")
    book = relationship("Book", backref="loans")
