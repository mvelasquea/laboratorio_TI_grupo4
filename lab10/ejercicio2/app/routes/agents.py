from fastapi import APIRouter
from app.config import OLLAMA_BASE_URL, OLLAMA_MODEL
from app.tools.inventory_tools import get_low_stock_products
from app.tools.logistics_tools import get_pending_shipments
from app.tools.forecast_tools import get_demand_forecast
from app.tools.executive_tools import get_company_kpis
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage

router = APIRouter()

llm = ChatOllama(model=OLLAMA_MODEL, base_url=OLLAMA_BASE_URL)


@router.post("/inventario")
def ejecutar_inventario():
    datos = get_low_stock_products()
    respuesta = llm.invoke([HumanMessage(content=f"Resume de forma clara y concisa estos productos con stock bajo:\n\n{datos}")])
    return {"status": "ok", "resultado": respuesta.content}


@router.post("/logistica")
def ejecutar_logistica():
    datos = get_pending_shipments()
    respuesta = llm.invoke([HumanMessage(content=f"Resume de forma clara y concisa estos envíos pendientes:\n\n{datos}")])
    return {"status": "ok", "resultado": respuesta.content}


@router.post("/pronosticos")
def ejecutar_pronosticos():
    datos = get_demand_forecast()
    respuesta = llm.invoke([HumanMessage(content=f"Resume de forma clara y concisa estos pronósticos de demanda:\n\n{datos}")])
    return {"status": "ok", "resultado": respuesta.content}


@router.post("/ejecutivo")
def ejecutar_ejecutivo():
    datos = get_company_kpis()
    respuesta = llm.invoke([HumanMessage(content=f"Resume de forma clara y concisa estos KPIs ejecutivos:\n\n{datos}")])
    return {"status": "ok", "resultado": respuesta.content}
