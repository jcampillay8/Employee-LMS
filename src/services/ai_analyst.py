import google.generativeai as genai
from src.core.config import settings

class AIAnalyst:
    def __init__(self):
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-2.5-flash')

    def ask_llm(self, data_context: str, question: str) -> str:
        prompt = f"""
        ROL: Eres un Analista de Datos Estratégicos especializado en LMS y RRHH para una importante minera en Chile (BHP/Escondida).
        CONTEXTO: Analizando métricas cruzadas de capacitación (LMS) y desempeño de Recursos Humanos.
        
        DATOS DE CONTEXTO (JSON/Tabla):
        {data_context}
        
        TAREA: Responder la pregunta de negocio utilizando enfoque de Gobernanza de Datos y Cumplimiento.
        
        REGLAS DE RESPUESTA:
        1. Considera siempre la distinción entre Personal Propio (Staff) y Contratistas (Contractors). El Staff tiene métricas de desempeño, los contratistas no.
        2. Si hay baja completación de cursos, relaciónalo con el impacto en el 'Performance Score' del Staff.
        3. Usa un tono ejecutivo, técnico y orientado a resultados.
        4. Sé conciso.

        PREGUNTA: {question}
        """
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"❌ Error en el análisis de IA: {str(e)}"

    def ask_llm_operational(self, user_id: str, activity_context: str, courses_context: str, question: str) -> str:
        prompt = f"""
        ROL: Administrador de Gobernanza LMS para minería.
        ACTIVO/TRABAJADOR: ID {user_id}
        
        CONTEXTO ACTIVIDAD Y RRHH:
        {activity_context}
        
        HISTORIAL DE CURSOS:
        {courses_context}
        
        TAREA: Analizar el estado de este trabajador (Staff o Contratista) y responder la consulta.
        
        REGLAS:
        1. Evalúa si el trabajador está atrasado en cursos de seguridad crítica.
        2. Revisa si la falta de capacitación está afectando su evaluación de desempeño (si es Staff).
        3. Da alertas si un curso lleva mucho tiempo incompleto.
        4. Sé directo y ofrece un diagnóstico claro.

        PREGUNTA DEL SUPERVISOR: {question}
        """
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"❌ Error en el análisis operativo: {str(e)}"