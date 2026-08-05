import os
import re
from google import genai
from google.genai import types
from sqlalchemy import text
from src.database.session import engine

# Database schema definitions for the prompt
DB_SCHEMA = """
Tables and schemas:
1. employees:
- emp_id (INTEGER)
- first_name (VARCHAR)
- last_name (VARCHAR)
- start_date (VARCHAR, e.g., '15-Feb-20')
- exit_date (VARCHAR, e.g., '14-Oct-22' or 'None')
- title (VARCHAR)
- supervisor (VARCHAR)
- ad_email (VARCHAR)
- business_unit (VARCHAR)
- employee_status (VARCHAR)
- employee_type (VARCHAR)
- pay_zone (VARCHAR)
- employee_classification_type (VARCHAR)
- department_type (VARCHAR)
- division (VARCHAR)
- dob (VARCHAR, e.g., '26-06-1984')
- state (VARCHAR)
- job_function (VARCHAR)
- gender_code (VARCHAR)
- race_desc (VARCHAR)
- marital_desc (VARCHAR)
- performance_score (VARCHAR)
- current_employee_rating (INTEGER)

2. hr_trainings:
- id (INTEGER)
- employee_id (INTEGER)
- training_date (VARCHAR)
- training_program_name (VARCHAR)
- training_type (VARCHAR)
- training_outcome (VARCHAR)
- location (VARCHAR)
- trainer (VARCHAR)
- duration_days (INTEGER)
- training_cost (FLOAT)

3. engagement_surveys:
- id (INTEGER)
- employee_id (INTEGER)
- survey_date (VARCHAR)
- engagement_score (FLOAT)
- satisfaction_score (FLOAT)
- work_life_balance_score (FLOAT)

4. recruitment:
- applicant_id (INTEGER)
- application_date (VARCHAR)
- first_name (VARCHAR)
- last_name (VARCHAR)
- gender (VARCHAR)
- dob (VARCHAR)
- phone (VARCHAR)
- email (VARCHAR)
- address (VARCHAR)
- city (VARCHAR)
- state (VARCHAR)
- zip_code (VARCHAR)
- country (VARCHAR)
- education_level (VARCHAR)
- years_of_experience (INTEGER)
- desired_salary (FLOAT)
- job_title (VARCHAR)
- status (VARCHAR)
"""

def generate_and_execute_sql(question: str, chat_history: list = None) -> str:
    """
    Takes a natural language question, generates a SQL query, executes it, 
    and returns a natural language response based on the result.
    """
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return "Error: GEMINI_API_KEY no está configurada."

    client = genai.Client(api_key=api_key)
    
    # Format chat history
    history_str = ""
    if chat_history:
        for msg in chat_history[-5:]: # Keep last 5 messages for context
            role = "User" if msg["role"] == "user" else "AI"
            history_str += f"{role}: {msg['text']}\n"
    
    # Step 1: Generate SQL Query
    sql_prompt = f"""
You are an expert PostgreSQL data analyst. Your task is to generate a SQL query based on the user's question.
Here is the database schema:
{DB_SCHEMA}

Return ONLY the raw SQL query. Do not include markdown formatting like ```sql or explanations. 
Ensure the query is compatible with PostgreSQL. For dates, remember they are strings and may need casting if performing math.
If the question is conceptual, a follow-up clarification, or cannot be answered with a SQL query based on the schema, reply with: "NO_SQL: <your answer or explanation directly in Spanish>".

Chat History:
{history_str}

User Question: {question}
"""
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=sql_prompt,
        )
        sql_query = response.text
        if sql_query is None:
            return f"Error: La respuesta del modelo está vacía. Detalles: {response}"
        sql_query = sql_query.strip()
        
        # Clean up any markdown blocks if the model accidentally includes them
        sql_query = re.sub(r'^```sql\s*', '', sql_query)
        sql_query = re.sub(r'^```\s*', '', sql_query)
        sql_query = re.sub(r'```$', '', sql_query).strip()
        
    except Exception as e:
        return f"Error al generar la consulta SQL: {e}"

    # Verify if it looks like a SQL query
    if not sql_query.strip().upper().startswith(("SELECT", "WITH")):
        # If it doesn't look like SQL, it's likely a natural language refusal or answer from the model.
        # Let's just return it directly to the user.
        return sql_query.replace("NO_SQL:", "").strip()

    # Step 2: Execute SQL Query
    try:
        with engine.connect() as conn:
            result = conn.execute(text(sql_query))
            rows = result.fetchall()
            
        if not rows:
            query_result = "No se encontraron resultados."
        else:
            # Format the output slightly for the LLM
            columns = result.keys()
            query_result = f"Columnas: {', '.join(columns)}\n"
            for row in rows[:50]: # Limit to 50 rows to prevent context overflow
                query_result += f"{row}\n"
                
    except Exception as e:
        return f"Error al ejecutar la consulta SQL: {e}"

    # Step 3: Generate Natural Language Response
    nl_prompt = f"""
You are an expert HR Data Analyst. 
A user asked the following question: "{question}"

Recent Chat History:
{history_str}

You ran the following SQL query to find the answer:
{sql_query}

The database returned the following results:
{query_result}

Please provide a clear, concise, and professional answer to the user's question IN SPANISH, based ONLY on the data provided. 
Do not explain the SQL query itself, just provide the answer.
"""
    try:
        final_response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=nl_prompt,
        )
        final_text = final_response.text
        if final_text is None:
            return f"Error: La respuesta final del modelo está vacía. Detalles: {final_response}"
        return final_text
    except Exception as e:
        return f"Error al generar la respuesta final: {e}"
