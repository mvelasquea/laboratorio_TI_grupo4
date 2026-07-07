from fastapi import APIRouter
from app.config import OLLAMA_BASE_URL, OLLAMA_MODEL
from app.tools.inventory_tools import get_low_stock_products
from app.tools.logistics_tools import get_pending_shipments
from app.tools.forecast_tools import get_demand_forecast
from app.tools.executive_tools import get_company_kpis
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage

router = APIRouter()

SYSTEM_PROMPT = """Eres un asistente de RetailNova Group, una corporación multinacional con más de 300 tiendas en Latinoamérica.

REGLAS ESTRICTAS:
1. SOLO puedes responder preguntas sobre la cadena de suministro, inventarios, logística, pronósticos y KPIs de RetailNova Group.
2. SI te preguntan sobre cualquier otro tema, responde: "Lo siento, solo puedo responder preguntas sobre la cadena de suministro de RetailNova Group."
3. NO inventes datos. Usa ÚNICAMENTE la información que te proporcionan.
4. Sé breve y conciso en tus respuestas.
5. Habla en español."""

llm = ChatOllama(model=OLLAMA_MODEL, base_url=OLLAMA_BASE_URL)


@router.post("/inventario")
def ejecutar_inventario():
    datos = get_low_stock_products()
    respuesta = llm.invoke([
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=f"Resume de forma clara y concisa estos productos con stock bajo de RetailNova:\n\n{datos}")
    ])
    return {"status": "ok", "resultado": respuesta.content}


@router.post("/logistica")
def ejecutar_logistica():
    datos = get_pending_shipments()
    respuesta = llm.invoke([
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=f"Resume de forma clara y concisa estos envíos pendientes de RetailNova:\n\n{datos}")
    ])
    return {"status": "ok", "resultado": respuesta.content}


@router.post("/pronosticos")
def ejecutar_pronosticos():
    datos = get_demand_forecast()
    respuesta = llm.invoke([
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=f"Resume de forma clara y concisa estos pronósticos de demanda de RetailNova:\n\n{datos}")
    ])
    return {"status": "ok", "resultado": respuesta.content}


@router.post("/ejecutivo")
def ejecutar_ejecutivo():
    datos = get_company_kpis()
    respuesta = llm.invoke([
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=f"Resume de forma clara y concisa estos KPIs ejecutivos de RetailNova:\n\n{datos}")
    ])
    return {"status": "ok", "resultado": respuesta.content}
