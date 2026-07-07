from app.config import OLLAMA_BASE_URL, OLLAMA_MODEL
from app.tools.inventory_tools import get_low_stock_products
from app.tools.logistics_tools import get_pending_shipments
from app.tools.forecast_tools import get_demand_forecast
from app.tools.executive_tools import get_company_kpis
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage

llm = ChatOllama(model=OLLAMA_MODEL, base_url=OLLAMA_BASE_URL)


def run_crew_analysis():
    inventario = get_low_stock_products()
    logistica = get_pending_shipments()
    pronostico = get_demand_forecast()
    kpis = get_company_kpis()

    prompt = f"""Eres un analista de RetailNova Group. Resume estos datos de forma clara:

INVENTARIO:
{inventario}

LOGISTICA:
{logistica}

PRONOSTICOS:
{pronostico}

KPIs:
{kpis}

Genera un resumen ejecutivo breve con los puntos más importantes."""

    respuesta = llm.invoke([HumanMessage(content=prompt)])
    return respuesta.content
