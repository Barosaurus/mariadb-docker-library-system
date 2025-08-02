from sqlalchemy import Column, Integer, String
from models.database import Base

class Book(Base):
    __tablename__ = "books"
    isbn = Column(String(13), primary_key=True, index=True)
    title = Column(String(255), index=True, nullable=False)
    author = Column(String(255), index=True, nullable=False)
    category = Column(String(100), index=True)
    publication_year = Column(Integer)
    available_copies = Column(Integer)
    total_copies = Column(Integer)