# 🏢 Employee-LMS: AI-Powered HR Analytics Dashboard

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![Dash](https://img.shields.io/badge/Dash-2.18+-009688.svg)](https://dash.plotly.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791.svg)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED.svg)](https://www.docker.com/)
[![Deployment](https://img.shields.io/badge/Deployed%20on-Railway-0b0d0e.svg)](https://railway.app)

Plataforma analítica avanzada orientada a Recursos Humanos (HR) que permite gestionar, visualizar y analizar datos del ciclo de vida de los empleados. Integrada con Inteligencia Artificial generativa para facilitar consultas "Text-to-SQL" directamente sobre la base de datos de talento.

📍 **Live Demo:** [Dashboard Online](https://predictivemaintenance-production.up.railway.app/dashboard/) *(Nota: Enlace de demostración provisional)*

---

## 🚀 Key Features

* **Advanced HR Dashboards:** Visualización interactiva de métricas clave como Tasa de Rotación (Attrition), Fuerza Laboral Activa, y Eficiencia de Capital usando **Dash** y **Plotly**.
* **AI Insights (Text-to-SQL):** Integración nativa con **Gemini 2.5 Flash** (mediante el nuevo SDK `google-genai`). Permite a los usuarios de negocio hacer preguntas en lenguaje natural (ej. "¿Cuál es el salario promedio en el departamento de IT?"), las cuales el modelo traduce a código SQL, ejecuta contra Postgres, y devuelve la respuesta analizada.
* **Context-Aware Chat:** Chatbot integrado en la interfaz (como panel lateral) capaz de retener el historial de conversación para preguntas de seguimiento y aclaraciones conceptuales.
* **Containerized Architecture:** Orquestación completa con **Docker Compose**, empaquetando el backend (Dash), la base de datos (PostgreSQL), y la carga inicial de datos.

---

## 🛠️ Architecture & Tech Stack

* **Language:** `Python 3.11+`
* **Frontend & UI:** `Dash`, `Dash Bootstrap Components`, `Plotly`.
* **Database & ORM:** `PostgreSQL 15`, `SQLAlchemy 2.0`.
* **AI/LLM Engine:** `Google Generative AI (Gemini 2.5 Flash)` vía SDK `google-genai`.
* **Infrastructure:** `Docker`, `Docker Compose`, preparativo para `Railway`.

---

## 📂 Project Structure

```plaintext
├── src/
│   ├── ai/             # Lógica RAG y Text-to-SQL (Gemini)
│   ├── core/           # Configuración de variables de entorno y settings
│   ├── database/       # Conexión, motor y sesión de SQLAlchemy
│   ├── models/         # Modelos relacionales de DB (Employee, Training, etc.)
│   ├── dashboard/      # Frontend: UI, Componentes, Layouts y Callbacks (Dash)
│   └── main.py         # Punto de entrada de la aplicación web
├── Data/               # Datasets originales (.csv, .xlsx)
├── scripts/            # Scripts de ingesta de datos a la BD
├── Dockerfile          # Configuración del contenedor de la aplicación
├── docker-compose.yml  # Orquestador de servicios (App + Database)
└── requirements.txt    # Dependencias de Python
```

## 🔧 Installation & Local Setup

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/jcampillay8/Employee-LMS.git
   cd Employee-LMS
   ```

2. **Configurar variables de entorno (`.env`):**
   Asegúrate de crear un archivo `.env` en la raíz del proyecto con los siguientes parámetros:
   ```env
   PROJECT_NAME="Employee LMS"
   DB_HOST=employee_lms_db
   DB_NAME=employee_db
   DB_USER=lms_user
   DB_PASSWORD=your_secure_password
   GEMINI_API_KEY=your_gemini_api_key
   PORT=8080
   ```

3. **Desplegar con Docker Compose:**
   ```bash
   docker compose build lms_app
   docker compose up -d
   ```
   La aplicación estará disponible en `http://localhost:8080/`.

---

## 📈 Strategic Impact

Este proyecto permite a los gerentes de RRHH y líderes de equipo:
* **Analizar la Retención:** Entender patrones de fuga de talento (Turnover) a través del tiempo.
* **Democratizar los Datos:** Eliminar la barrera técnica permitiendo que cualquier usuario obtenga respuestas de los datos usando lenguaje natural, sin saber SQL.
* **Visibilidad de Capacitación:** Mapear el retorno de inversión y el progreso de entrenamiento corporativo.

---

## 👨‍💻 Author

**Jaime Campillay** - *Data & Software Engineer* 🔗 [LinkedIn](https://www.linkedin.com/in/jaime-campillay/)