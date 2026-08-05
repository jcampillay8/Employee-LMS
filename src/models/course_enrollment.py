from sqlalchemy import String, Integer, Float, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database.base import Base

class CourseEnrollment(Base):
    __tablename__ = "course_enrollments"
    
    enrollment_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[str] = mapped_column(String, ForeignKey("workers.user_id"))
    course_id: Mapped[int] = mapped_column(Integer)
    enrolled_at: Mapped[str] = mapped_column(String, nullable=True)
    completed_at: Mapped[str] = mapped_column(String, nullable=True)
    progress_pct: Mapped[float] = mapped_column(Float, nullable=True)
    source_channel: Mapped[str] = mapped_column(String, nullable=True)
