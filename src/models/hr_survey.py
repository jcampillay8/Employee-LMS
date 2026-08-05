from sqlalchemy import Column, String, Integer, ForeignKey
from src.database.base import Base

class HRSurvey(Base):
    __tablename__ = "hr_engagement_surveys"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, ForeignKey("workers.user_id"), index=True)
    survey_date = Column(String)
    engagement_score = Column(Integer)
    satisfaction_score = Column(Integer)
    work_life_balance_score = Column(Integer)
