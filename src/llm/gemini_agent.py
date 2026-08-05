# src/llm/gemini_agent.py

import os

class GeminiAgent:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        # Initialize the model here when ready
        pass

    def get_insights(self, query: str, context: dict) -> str:
        """
        Takes a user query and a context dictionary (like current dashboard data)
        and returns a response from Gemini.
        """
        if not self.api_key:
            return "Error: GEMINI_API_KEY no configurada."
        
        # Placeholder para la llamada real a Gemini API
        return f"Gemini Analysis for query: '{query}'. (Funcionalidad próximamente)"
