from sqlalchemy import Column, Integer, String, Date, Enum
from sqlalchemy.sql import func
from models.database import Base
import enum


class UserStatus(enum.Enum):
    active = "active"
    inactive = "inactive"
    suspended = "suspended"

class User(Base):
    __tablename__ = "users"
    user_number = Column(String(20), primary_key=True, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    phone = Column(String(20))
    registration_date = Column(Date, default=func.current_date())
    status = Column(Enum(UserStatus), default=UserStatus.active)