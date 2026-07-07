from crewai import Agent, LLM
from app.config import GROQ_API_KEY
from app.tools.inventory_tools import (
    get_low_stock_products,
    get_inventory_by_store,
    calculate_reorder_point,
    get_stock_movements,
)
from app.tools.logistics_tools import (
    get_pending_shipments,
    get_logistics_costs,
    get_delivery_performance,
    get_suppliers_ranking,
)
from app.tools.forecast_tools import (
    get_demand_forecast,
    get_forecast_accuracy,
    get_sales_trends,
    get_top_products,
)
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

analista_operaciones = Agent(
    role="Analista de Operaciones",
    goal="Analizar inventarios, logística y pronósticos de RetailNova Group.",
    backstory="Eres un analista que revisa el estado operativo de la cadena de suministro.",
    tools=[
        get_low_stock_products,
        get_pending_shipments,
        get_logistics_costs,
        get_demand_forecast,
        get_company_kpis,
        get_alerts,
    ],
    llm=llm,
    verbose=True,
    allow_delegation=False,
    max_iter=3,
)

agente_ejecutivo = Agent(
    role="Agente Ejecutivo",
    goal="Generar un resumen ejecutivo con las findings del analista.",
    backstory="Eres el asistente ejecutivo que consolida reportes para la dirección.",
    tools=[],
    llm=llm,
    verbose=True,
    allow_delegation=False,
    max_iter=2,
)
