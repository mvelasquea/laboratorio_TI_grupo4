from fastapi import APIRouter
from app.config import OLLAMA_BASE_URL, OLLAMA_MODEL
from app.tools.inventory_tools import get_low_stock_products
from app.tools.logistics_tools import get_pending_shipments
from app.tools.forecast_tools import get_demand_forecast
from app.tools.executive_tools import get_company_kpis
import requests

router = APIRouter()


def _call_ollama(prompt):
    try:
        response = requests.post(
            f"{OLLAMA_BASE_URL}/api/generate",
            json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False,
            },
            timeout=30,
        )
        return response.json().get("response", "Sin respuesta")
    except Exception as e:
        return f"Error al conectar con Ollama: {str(e)}"


@router.post("/inventario")
def ejecutar_inventario():
    datos = get_low_stock_products()
    prompt = f"Resume estos productos con stock bajo de forma clara y concisa:\n\n{datos}"
    respuesta = _call_ollama(prompt)
    return {"status": "ok", "resultado": respuesta}


@router.post("/logistica")
def ejecutar_logistica():
    datos = get_pending_shipments()
    prompt = f"Resume estos envíos pendientes de forma clara y concisa:\n\n{datos}"
    respuesta = _call_ollama(prompt)
    return {"status": "ok", "resultado": respuesta}


@router.post("/pronosticos")
def ejecutar_pronosticos():
    datos = get_demand_forecast()
    prompt = f"Resume estos pronósticos de demanda de forma clara y concisa:\n\n{datos}"
    respuesta = _call_ollama(prompt)
    return {"status": "ok", "resultado": respuesta}


@router.post("/ejecutivo")
def ejecutar_ejecutivo():
    datos = get_company_kpis()
    prompt = f"Resume estos KPIs ejecutivos de forma clara y concisa:\n\n{datos}"
    respuesta = _call_ollama(prompt)
    return {"status": "ok", "resultado": respuesta}
