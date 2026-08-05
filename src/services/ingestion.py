import logging
import polars as pl
from sqlalchemy.orm import Session

from src.core.config import settings
from src.database.session import engine, SessionLocal
from src.database.base import Base
from src.models.worker import Worker
from src.models.employee_profile import EmployeeProfile
from src.models.course_enrollment import CourseEnrollment
from src.models.daily_activity_log import DailyActivityLog
from src.models.hr_training import HRTraining
from src.models.hr_survey import HRSurvey

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_tables():
    logger.info(f"🛠 Conectando a {settings.DB_HOST} para crear tablas...")
    Base.metadata.create_all(bind=engine)
    logger.info("✅ Tablas verificadas/creadas con éxito.")

def ingest_csv_to_db():
    db: Session = SessionLocal()
    
    try:
        if not db.query(Worker).first():
            logger.info("🚀 Cargando Workers (Staff & Contractors) y Perfiles de RRHH...")
            
            # 1. Leer Users del LMS
            lms_path = settings.DATA_PATH / "lms_users.csv"
            df_users = pl.read_csv(lms_path)
            df_users = df_users.with_columns(pl.col("is_active").cast(pl.Boolean))
            if "created_at" in df_users.columns:
                df_users = df_users.drop("created_at")
                
            # 2. Asignar 'Staff' a los primeros 3000 y 'Contractor' al resto
            total_users = df_users.height
            staff_count = 3000
            
            worker_types = ["Staff"] * staff_count + ["Contractor"] * (total_users - staff_count)
            df_users = df_users.with_columns(pl.Series("worker_type", worker_types))
            
            # Insertar Workers
            db.bulk_insert_mappings(Worker, df_users.to_dicts())
            db.commit()
            logger.info(f"✅ {df_users.height} workers cargados.")

            # 3. Cargar HR Employee Data
            hr_path = settings.DATA_PATH / "employee_hr" / "employee_data.csv"
            df_hr = pl.read_csv(hr_path)
            
            staff_ids = df_users.head(staff_count)["user_id"].to_list()
            
            df_hr = df_hr.rename({
                "EmpID": "emp_id",
                "FirstName": "first_name",
                "LastName": "last_name",
                "Title": "title",
                "DepartmentType": "department",
                "Performance Score": "performance_score",
                "Current Employee Rating": "current_rating"
            }).select(["emp_id", "first_name", "last_name", "title", "department", "performance_score", "current_rating"])
            
            df_hr = df_hr.with_columns(pl.col("emp_id").cast(pl.Utf8))
            df_hr = df_hr.with_columns(pl.Series("user_id", staff_ids))
            
            db.bulk_insert_mappings(EmployeeProfile, df_hr.to_dicts())
            db.commit()
            logger.info(f"✅ {df_hr.height} perfiles de RRHH cargados.")

            # Crear mapeo de EmpID a UUID para poder enlazar las siguientes tablas de RRHH
            mapping_dict = dict(zip(df_hr["emp_id"].to_list(), staff_ids))

            # 4. Cargar HR Training
            hr_training_path = settings.DATA_PATH / "employee_hr" / "training_and_development_data.csv"
            df_train = pl.read_csv(hr_training_path)
            df_train = df_train.rename({
                "Employee ID": "emp_id",
                "Training Date": "training_date",
                "Training Program Name": "training_program_name",
                "Training Type": "training_type",
                "Training Outcome": "training_outcome",
                "Location": "location",
                "Trainer": "trainer",
                "Training Duration(Days)": "duration_days",
                "Training Cost": "cost"
            })
            df_train = df_train.with_columns(pl.col("emp_id").cast(pl.Utf8))
            # Mapear EmpID a UUID
            df_train = df_train.with_columns(
                pl.col("emp_id").replace_strict(mapping_dict, default=None).alias("user_id")
            ).drop("emp_id")
            
            # Limpiar filas con user_id null por si acaso
            df_train = df_train.filter(pl.col("user_id").is_not_null())
            db.bulk_insert_mappings(HRTraining, df_train.to_dicts())
            db.commit()
            logger.info(f"✅ {df_train.height} cursos especiales de RRHH cargados.")

            # 5. Cargar HR Surveys
            hr_survey_path = settings.DATA_PATH / "employee_hr" / "employee_engagement_survey_data.csv"
            df_survey = pl.read_csv(hr_survey_path)
            df_survey = df_survey.rename({
                "Employee ID": "emp_id",
                "Survey Date": "survey_date",
                "Engagement Score": "engagement_score",
                "Satisfaction Score": "satisfaction_score",
                "Work-Life Balance Score": "work_life_balance_score"
            })
            df_survey = df_survey.with_columns(pl.col("emp_id").cast(pl.Utf8))
            # Mapear EmpID a UUID
            df_survey = df_survey.with_columns(
                pl.col("emp_id").replace_strict(mapping_dict, default=None).alias("user_id")
            ).drop("emp_id")
            
            df_survey = df_survey.filter(pl.col("user_id").is_not_null())
            db.bulk_insert_mappings(HRSurvey, df_survey.to_dicts())
            db.commit()
            logger.info(f"✅ {df_survey.height} encuestas de RRHH cargadas.")

        if not db.query(CourseEnrollment).first():
            logger.info("🚀 Cargando Enrollments Operativos...")
            path = settings.DATA_PATH / "course_enrollments.csv"
            df = pl.read_csv(path)
            if "enrollment_id" in df.columns:
                df = df.drop("enrollment_id")
            if "created_at" in df.columns:
                df = df.drop("created_at")
            db.bulk_insert_mappings(CourseEnrollment, df.to_dicts())
            db.commit()
            logger.info(f"✅ {df.height} enrollments operativos cargados.")

        if not db.query(DailyActivityLog).first():
            logger.info("🚀 Cargando Activity Logs (puede tardar un minuto)...")
            path = settings.DATA_PATH / "daily_activity_logs.csv"
            df = pl.read_csv(path)
            
            if "activity_id" in df.columns:
                df = df.drop("activity_id")
            if "created_at" in df.columns:
                df = df.drop("created_at")
                
            chunk_size = 50000
            for i in range(0, df.height, chunk_size):
                chunk = df.slice(i, chunk_size).to_dicts()
                db.bulk_insert_mappings(DailyActivityLog, chunk)
                db.commit()
                logger.info(f"📦 Progress: {min(i + chunk_size, df.height)} logs...")

    except Exception as e:
        logger.error(f"❌ Error durante la ingesta: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_tables()
    ingest_csv_to_db()
    logger.info("🎉 Ingesta completada!")