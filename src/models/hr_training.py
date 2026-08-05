from sqlalchemy import Column, String, Integer, Float, ForeignKey
from src.database.base import Base

class HRTraining(Base):
    __tablename__ = "hr_trainings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, ForeignKey("workers.user_id"), index=True)
    training_date = Column(String)
    training_program_name = Column(String)
    training_type = Column(String)
    training_outcome = Column(String)
    location = Column(String)
    trainer = Column(String)
    duration_days = Column(Integer)
    cost = Column(Float)
