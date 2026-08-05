from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Date, Boolean
from sqlalchemy.ext.declarative import declarative_base
from src.database.base import Base

class Employee(Base):
    __tablename__ = "employees"
    
    emp_id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String)
    start_date = Column(String)
    exit_date = Column(String, nullable=True)
    title = Column(String)
    supervisor = Column(String)
    email = Column(String)
    business_unit = Column(String)
    employee_status = Column(String)
    employee_type = Column(String) # e.g., Contract, Full-time
    department_type = Column(String)
    division = Column(String)
    dob = Column(String)
    state = Column(String)
    job_function = Column(String)
    gender_code = Column(String)
    race_desc = Column(String)
    marital_desc = Column(String)
    performance_score = Column(String)
    current_employee_rating = Column(Integer)

class EngagementSurvey(Base):
    __tablename__ = "engagement_surveys"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    employee_id = Column(Integer, ForeignKey("employees.emp_id"))
    survey_date = Column(String)
    engagement_score = Column(Float) # can be float if mean, but original says 5, 2, 4 etc. Float is safer.
    satisfaction_score = Column(Float)
    work_life_balance_score = Column(Float)

class HRTraining(Base):
    __tablename__ = "hr_trainings"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    employee_id = Column(Integer, ForeignKey("employees.emp_id"))
    training_date = Column(String)
    training_program_name = Column(String)
    training_type = Column(String)
    training_outcome = Column(String)
    location = Column(String)
    trainer = Column(String)
    duration_days = Column(Integer)
    training_cost = Column(Float)

class Recruitment(Base):
    __tablename__ = "recruitment"
    
    applicant_id = Column(Integer, primary_key=True, index=True)
    application_date = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    gender = Column(String)
    dob = Column(String)
    phone = Column(String)
    email = Column(String)
    address = Column(String)
    city = Column(String)
    state = Column(String)
    zip_code = Column(String)
    country = Column(String)
    education_level = Column(String)
    years_of_experience = Column(Integer)
    desired_salary = Column(Float)
    job_title = Column(String)
    status = Column(String)
