from app.config import OLLAMA_BASE_URL, OLLAMA_MODEL
from app.tools.inventory_tools import get_low_stock_products
from app.tools.logistics_tools import get_pending_shipments
from app.tools.forecast_tools import get_demand_forecast
from app.tools.executive_tools import get_company_kpis
import requests


def _call_ollama(prompt):
    try:
        response = requests.post(
            f"{OLLAMA_BASE_URL}/api/generate",
            json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False,
            },
            timeout=60,
        )
        return response.json().get("response", "Sin respuesta")
    except Exception as e:
        return f"Error al conectar con Ollama: {str(e)}"


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
    return _call_ollama(prompt)
