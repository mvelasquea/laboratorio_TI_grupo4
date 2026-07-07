from fastapi import APIRouter
from app.config import OLLAMA_BASE_URL, OLLAMA_MODEL
from app.tools.db_queries import query_low_stock_products, query_pending_shipments, query_demand_forecast, query_company_kpis
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage

router = APIRouter()

SYSTEM_PROMPT = """Eres un asistente de RetailNova Group, corporación con más de 300 tiendas en Latinoamérica.

REGLAS:
1. SOLO responde sobre cadena de suministro, inventarios, logística, pronósticos y KPIs de RetailNova.
2. Si te preguntan de otro tema: "Solo puedo responder sobre la cadena de suministro de RetailNova Group."
3. NO inventes datos.
4. Sé breve. Habla en español."""

llm = ChatOllama(model=OLLAMA_MODEL, base_url=OLLAMA_BASE_URL)


@router.post("/inventario")
def ejecutar_inventario():
    datos = query_low_stock_products()
    respuesta = llm.invoke([
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=f"Resume estos productos con stock bajo:\n\n{datos}")
    ])
    return {"status": "ok", "resultado": respuesta.content}


@router.post("/logistica")
def ejecutar_logistica():
    datos = query_pending_shipments()
    respuesta = llm.invoke([
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=f"Resume estos envíos pendientes:\n\n{datos}")
    ])
    return {"status": "ok", "resultado": respuesta.content}


@router.post("/pronosticos")
def ejecutar_pronosticos():
    datos = query_demand_forecast()
    respuesta = llm.invoke([
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=f"Resume estos pronósticos de demanda:\n\n{datos}")
    ])
    return {"status": "ok", "resultado": respuesta.content}


@router.post("/ejecutivo")
def ejecutar_ejecutivo():
    datos = query_company_kpis()
    respuesta = llm.invoke([
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=f"Resume estos KPIs ejecutivos:\n\n{datos}")
    ])
    return {"status": "ok", "resultado": respuesta.content}
