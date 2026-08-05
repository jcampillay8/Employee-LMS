from sqlalchemy import Column, String, Boolean
from src.database.base import Base

class Worker(Base):
    __tablename__ = "workers"

    user_id = Column(String, primary_key=True, index=True)
    worker_type = Column(String, nullable=False) # 'Staff' or 'Contractor'
    acquisition_channel = Column(String)
    is_active = Column(Boolean, default=True)
    plan_tier = Column(String)
