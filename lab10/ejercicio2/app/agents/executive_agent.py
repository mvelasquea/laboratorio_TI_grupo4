from crewai import Agent, LLM
from app.config import GROQ_API_KEY
from app.tools.executive_tools import (
    get_company_kpis,
    get_store_performance,
    get_financial_summary,
    get_alerts,
)

llm = LLM(
    model="groq/llama-3.1-8b-instant",
    api_key=GROQ_API_KEY,
)

executive_agent = Agent(
    role="Agente Ejecutivo",
    goal="Consolidar información de inventarios, logística y pronósticos "
         "para generar reportes ejecutivos y recomendaciones estratégicas.",
    backstory=(
        "Eres el asistente ejecutivo senior de RetailNova Group. Tu función "
        "es consolidar los análisis de los demás agentes y presentar un resumen "
        "ejecutivo claro para la dirección. Tienes acceso a KPIs, métricas "
        "financieras y alertas críticas de toda la operación."
    ),
    tools=[
        get_company_kpis,
        get_store_performance,
        get_financial_summary,
        get_alerts,
    ],
    llm=llm,
    verbose=True,
    allow_delegation=False,
    max_iter=5,
)
