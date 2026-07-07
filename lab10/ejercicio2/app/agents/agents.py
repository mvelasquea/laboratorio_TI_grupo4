from crewai import Agent, LLM
from app.config import GROQ_API_KEY
from app.tools.inventory_tools import (
    get_low_stock_products,
    calculate_reorder_point,
)
from app.tools.logistics_tools import (
    get_pending_shipments,
    get_logistics_costs,
)
from app.tools.forecast_tools import (
    get_demand_forecast,
    get_forecast_accuracy,
)
from app.tools.executive_tools import (
    get_company_kpis,
    get_alerts,
)

llm = LLM(
    model="groq/llama-3.1-8b-instant",
    api_key=GROQ_API_KEY,
)

inventory_agent = Agent(
    role="Analista de Inventarios",
    goal="Identificar productos con stock bajo y recomendar reabastecimiento.",
    backstory="Experto en inventarios retail. Detecta roturas de stock.",
    tools=[get_low_stock_products, calculate_reorder_point],
    llm=llm,
    verbose=True,
    allow_delegation=False,
    max_iter=2,
)

logistics_agent = Agent(
    role="Especialista en Logística",
    goal="Revisar envíos pendientes y costos logísticos.",
    backstory="Ingeniero logístico. Optimiza distribución y costos.",
    tools=[get_pending_shipments, get_logistics_costs],
    llm=llm,
    verbose=True,
    allow_delegation=False,
    max_iter=2,
)

forecast_agent = Agent(
    role="Analista de Pronósticos",
    goal="Evaluar demanda y precisión de pronósticos.",
    backstory="Data scientist de demanda retail. Analiza tendencias.",
    tools=[get_demand_forecast, get_forecast_accuracy],
    llm=llm,
    verbose=True,
    allow_delegation=False,
    max_iter=2,
)

executive_agent = Agent(
    role="Agente Ejecutivo",
    goal="Generar resumen ejecutivo con KPIs y alertas.",
    backstory="Asistente ejecutivo. Consolida reportes para dirección.",
    tools=[get_company_kpis, get_alerts],
    llm=llm,
    verbose=True,
    allow_delegation=False,
    max_iter=2,
)
