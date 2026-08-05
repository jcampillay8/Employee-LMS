from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database.base import Base

class DailyActivityLog(Base):
    __tablename__ = "daily_activity_logs"
    
    activity_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[str] = mapped_column(String, ForeignKey("workers.user_id"))
    activity_date: Mapped[str] = mapped_column(String, nullable=True)
    minutes_learned: Mapped[int] = mapped_column(Integer, nullable=True, default=0)
    lessons_completed: Mapped[int] = mapped_column(Integer, nullable=True, default=0)
