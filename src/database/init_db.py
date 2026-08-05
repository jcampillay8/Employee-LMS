import os
import pandas as pd
from src.database.session import engine, SessionLocal
from src.database.base import Base
from src.database.models import Employee, EngagementSurvey, HRTraining, Recruitment

def init_db():
    print("Creating tables...")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    
    print("Populating data from CSVs...")
    with SessionLocal() as db:
        # Check if already populated
        if db.query(Employee).count() == 0:
            data_dir = "/app/Data"
            
            # 1. Employees
            emp_df = pd.read_csv(f"{data_dir}/employee_data.csv")
            for _, row in emp_df.iterrows():
                emp = Employee(
                    emp_id=row['EmpID'],
                    first_name=row['FirstName'],
                    last_name=row['LastName'],
                    start_date=row['StartDate'],
                    exit_date=row['ExitDate'] if pd.notna(row['ExitDate']) else None,
                    title=row['Title'],
                    supervisor=row['Supervisor'],
                    email=row['ADEmail'],
                    business_unit=row['BusinessUnit'],
                    employee_status=row['EmployeeStatus'],
                    employee_type=row['EmployeeType'],
                    department_type=row['DepartmentType'],
                    division=row['Division'],
                    dob=row['DOB'],
                    state=row['State'],
                    job_function=row['JobFunctionDescription'],
                    gender_code=row['GenderCode'],
                    race_desc=row['RaceDesc'],
                    marital_desc=row['MaritalDesc'],
                    performance_score=row['Performance Score'],
                    current_employee_rating=row['Current Employee Rating'] if pd.notna(row['Current Employee Rating']) else None
                )
                db.add(emp)
            db.commit()
            print(f"Inserted {len(emp_df)} employees.")

            # Precargar todos los IDs válidos para evitar N+1 queries
            valid_emp_ids = {emp.emp_id for emp in db.query(Employee.emp_id).all()}

            # 2. Engagement Surveys
            eng_df = pd.read_csv(f"{data_dir}/employee_engagement_survey_data.csv")
            for _, row in eng_df.iterrows():
                # verify employee exists
                if row['Employee ID'] in valid_emp_ids:
                    surv = EngagementSurvey(
                        employee_id=row['Employee ID'],
                        survey_date=row['Survey Date'],
                        engagement_score=row['Engagement Score'],
                        satisfaction_score=row['Satisfaction Score'],
                        work_life_balance_score=row['Work-Life Balance Score']
                    )
                    db.add(surv)
            db.commit()
            print(f"Inserted {len(eng_df)} engagement surveys.")

            # 3. Trainings
            train_df = pd.read_csv(f"{data_dir}/training_and_development_data.csv")
            for _, row in train_df.iterrows():
                # verify employee exists
                if row['Employee ID'] in valid_emp_ids:
                    train = HRTraining(
                        employee_id=row['Employee ID'],
                        training_date=row['Training Date'],
                        training_program_name=row['Training Program Name'],
                        training_type=row['Training Type'],
                        training_outcome=row['Training Outcome'],
                        location=row['Location'],
                        trainer=row['Trainer'],
                        duration_days=row['Training Duration(Days)'],
                        training_cost=row['Training Cost']
                    )
                    db.add(train)
            db.commit()
            print(f"Inserted {len(train_df)} trainings.")

            # 4. Recruitment
            if os.path.exists(f"{data_dir}/recruitment_data.csv"):
                rec_df = pd.read_csv(f"{data_dir}/recruitment_data.csv")
                for _, row in rec_df.iterrows():
                    rec = Recruitment(
                        applicant_id=row['Applicant ID'],
                        application_date=row['Application Date'],
                        first_name=row['First Name'],
                        last_name=row['Last Name'],
                        gender=row['Gender'],
                        dob=row['Date of Birth'],
                        phone=row['Phone Number'],
                        email=row['Email'],
                        address=row['Address'],
                        city=row['City'],
                        state=row['State'],
                        zip_code=row['Zip Code'],
                        country=row['Country'],
                        education_level=row['Education Level'],
                        years_of_experience=row['Years of Experience'],
                        desired_salary=row['Desired Salary'],
                        job_title=row['Job Title'],
                        status=row['Status']
                    )
                    db.add(rec)
                db.commit()
                print(f"Inserted {len(rec_df)} recruitment records.")

    print("Database initialization complete.")

if __name__ == "__main__":
    init_db()
