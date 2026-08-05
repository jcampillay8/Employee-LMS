from sqlalchemy import Column, String, Integer, ForeignKey
from src.database.base import Base

class EmployeeProfile(Base):
    __tablename__ = "employee_profiles"

    emp_id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey("workers.user_id"), unique=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    title = Column(String)
    department = Column(String)
    performance_score = Column(String)
    current_rating = Column(Integer)
