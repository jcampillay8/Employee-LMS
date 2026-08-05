import pandas as pd
from sqlalchemy import text
from src.database.session import engine

def get_turnover_rate():
    """Calculates the turnover rate (like turnover2 in notebook)."""
    query = """
    SELECT  COUNT(emp_id) AS total_count,
            SUM(CASE WHEN employee_status IN ('Terminated for Cause', 'Voluntarily Terminated') 
                     THEN 1 ELSE 0 END) AS Terminated,
            ROUND(
                100.0 * SUM(CASE WHEN employee_status IN ('Terminated for Cause', 'Voluntarily Terminated')
                                 THEN 1 ELSE 0 END) / COUNT(emp_id), 
                2
            ) AS turnover_rate
    FROM employees
    """
    with engine.connect() as conn:
        df = pd.read_sql(text(query), conn)
    return df

def get_recruitment_status():
    """Gets the monthly recruitment status (like recruitment_status in notebook)."""
    # PostgreSQL syntax for dates instead of SQLite's substr/case.
    # The application_date format in db is 'DD-Mon-YY' e.g. '04-Jan-22'.
    # We can cast it to date in Postgres.
    query = """
    SELECT
        TO_CHAR(TO_DATE(application_date, 'DD-Mon-YY'), 'YYYY-MM') AS month,
        COUNT(CASE WHEN status = 'Applied' THEN 1 END) AS applied,
        COUNT(CASE WHEN status = 'Interviewing' THEN 1 END) AS interviewing,
        COUNT(CASE WHEN status = 'In Review' THEN 1 END) AS under_review,
        COUNT(CASE WHEN status = 'Rejected' THEN 1 END) AS rejected,
        COUNT(CASE WHEN status = 'Offered' THEN 1 END) AS offered
    FROM recruitment
    WHERE TO_CHAR(TO_DATE(application_date, 'DD-Mon-YY'), 'YYYY-MM') != '2023-08'
    GROUP BY month
    ORDER BY month
    """
    with engine.connect() as conn:
        df = pd.read_sql(text(query), conn)
    return df

def get_training_costs():
    """Gets total training costs by program."""
    query = """
    SELECT
        training_program_name AS program,
        SUM(training_cost) AS total_cost
    FROM hr_trainings
    GROUP BY training_program_name
    ORDER BY total_cost DESC
    """
    with engine.connect() as conn:
        df = pd.read_sql(text(query), conn)
    return df

def get_training_programs():
    """Gets total number of trainings conducted for each program."""
    query = """
    SELECT
        training_program_name AS "Training Program Name",
        COUNT(*) AS total_trainings,
        ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM hr_trainings) , 2) AS total_percentage
    FROM hr_trainings
    GROUP BY training_program_name
    ORDER BY total_trainings DESC
    """
    with engine.connect() as conn:
        df = pd.read_sql(text(query), conn)
    return df

def get_frequency_per_year():
    """Yearly frequency and outcomes of trainings."""
    query = """
    SELECT
        TO_CHAR(TO_DATE(training_date, 'DD-Mon-YY'), 'YYYY') AS year,
        training_program_name AS program,
        COUNT(employee_id) AS yearly_trainings,
        SUM(training_cost) AS training_costs,
        ROUND(SUM(CASE WHEN training_outcome = 'Passed' THEN 1 ELSE 0 END)* 100.0 / COUNT(*), 2) AS passed_rate,
        ROUND(SUM(CASE WHEN training_outcome = 'Failed' THEN 1 ELSE 0 END)* 100.0 / COUNT(*), 2) AS failed_rate,
        ROUND(SUM(CASE WHEN training_outcome = 'Completed' THEN 1 ELSE 0 END)* 100.0 / COUNT(*), 2) AS pending_assessment_rate,
        ROUND(SUM(CASE WHEN training_outcome = 'Incomplete' THEN 1 ELSE 0 END)* 100.0 / COUNT(*), 2) AS incomplete_rate
    FROM hr_trainings
    GROUP BY year, program
    ORDER BY year, program
    """
    with engine.connect() as conn:
        df = pd.read_sql(text(query), conn)
    return df

def get_frequency_per_month():
    """Monthly frequency of trainings."""
    query = """
    SELECT
        TO_CHAR(TO_DATE(training_date, 'DD-Mon-YY'), 'MM') AS month,
        TO_CHAR(TO_DATE(training_date, 'DD-Mon-YY'), 'YYYY') AS year,
        training_program_name AS "Training Program Name",
        COUNT(employee_id) AS monthly_trainings,
        SUM(training_cost) AS training_costs,
        ROUND(SUM(CASE WHEN training_outcome = 'Passed' THEN 1 ELSE 0 END)* 100.0 / COUNT(*), 2) AS passed_rate,
        ROUND(SUM(CASE WHEN training_outcome = 'Failed' THEN 1 ELSE 0 END)* 100.0 / COUNT(*), 2) AS failed_rate,
        ROUND(SUM(CASE WHEN training_outcome = 'Completed' THEN 1 ELSE 0 END)* 100.0 / COUNT(*), 2) AS pending_assessment_rate,
        ROUND(SUM(CASE WHEN training_outcome = 'Incomplete' THEN 1 ELSE 0 END)* 100.0 / COUNT(*), 2) AS incomplete_rate
    FROM hr_trainings
    GROUP BY year, month, "Training Program Name"
    ORDER BY year, month, "Training Program Name"
    """
    with engine.connect() as conn:
        df = pd.read_sql(text(query), conn)
    return df

def get_turnover_by_division():
    """Gets turnover rate by division."""
    query = """
    SELECT  
        division,
        COUNT(emp_id) AS total_count,
        SUM(CASE WHEN employee_status IN ('Terminated for Cause', 'Voluntarily Terminated') 
                 THEN 1 ELSE 0 END) AS Terminated,
        ROUND(
            100.0 * SUM(CASE WHEN employee_status IN ('Terminated for Cause', 'Voluntarily Terminated')
                             THEN 1 ELSE 0 END) / COUNT(emp_id),
            2
        ) AS turnover_rate
    FROM employees
    GROUP BY division
    ORDER BY turnover_rate DESC
    """
    with engine.connect() as conn:
        df = pd.read_sql(text(query), conn)
    return df

def get_tenure():
    """Gets tenure in months for terminated employees."""
    query = """
    SELECT
        ROUND(
            CAST(
                (TO_DATE(exit_date, 'DD-Mon-YY') - TO_DATE(start_date, 'DD-Mon-YY')) AS numeric
            ) / 30.44, 1
        ) AS tenure_months
    FROM employees
    WHERE exit_date IS NOT NULL AND exit_date != 'None' 
      AND (TO_DATE(exit_date, 'DD-Mon-YY') - TO_DATE(start_date, 'DD-Mon-YY')) > 30
    """
    with engine.connect() as conn:
        df = pd.read_sql(text(query), conn)
    return df

def get_individual_engagement_scores():
    """Gets individual engagement scores joined with performance data."""
    query = """
    SELECT  
        e.division,
        s.engagement_score AS "Engagement Score",
        s.satisfaction_score AS "Satisfaction Score",
        s.work_life_balance_score AS "Work-Life Balance Score",
        e.current_employee_rating,
        e.performance_score AS "Performance Score"
    FROM engagement_surveys s
    LEFT JOIN employees e ON s.employee_id = e.emp_id
    WHERE e.performance_score IS NOT NULL
    """
    with engine.connect() as conn:
        df = pd.read_sql(text(query), conn)
    return df
