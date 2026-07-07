from fastapi import APIRouter
from app.config import OLLAMA_BASE_URL, OLLAMA_MODEL
from app.tools.db_queries import (
    query_low_stock_products,
    query_pending_shipments,
    query_demand_forecast,
    query_company_kpis,
    query_alerts,
)
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage

router = APIRouter()

llm = ChatOllama(model=OLLAMA_MODEL, base_url=OLLAMA_BASE_URL)


@router.post("/inventario")
def ejecutar_inventario():
    datos = query_low_stock_products()
    respuesta = llm.invoke([
        SystemMessage(content="Eres un analista de inventarios de RetailNova. Resume brevemente estos productos con stock bajo. Habla en español."),
        HumanMessage(content=f"Datos de inventario:\n{datos}")
    ])
    return {"status": "ok", "resultado": respuesta.content}


@router.post("/logistica")
def ejecutar_logistica():
    datos = query_pending_shipments()
    respuesta = llm.invoke([
        SystemMessage(content="Eres un especialista en logística de RetailNova. Resume brevemente estos envíos pendientes. Habla en español."),
        HumanMessage(content=f"Datos de logística:\n{datos}")
    ])
    return {"status": "ok", "resultado": respuesta.content}


@router.post("/pronosticos")
def ejecutar_pronosticos():
    datos = query_demand_forecast()
    respuesta = llm.invoke([
        SystemMessage(content="Eres un analista de pronósticos de RetailNova. Resume brevemente estos datos de demanda. Habla en español."),
        HumanMessage(content=f"Datos de pronósticos:\n{datos}")
    ])
    return {"status": "ok", "resultado": respuesta.content}


@router.post("/ejecutivo")
def ejecutar_ejecutivo():
    kpis = query_company_kpis()
    alertas = query_alerts()
    respuesta = llm.invoke([
        SystemMessage(content="Eres un asistente ejecutivo de RetailNova. Resume brevemente estos KPIs y alertas. Habla en español."),
        HumanMessage(content=f"KPIs:\n{kpis}\n\nAlertas:\n{alertas}")
    ])
    return {"status": "ok", "resultado": respuesta.content}


@router.post("/chat/{agente}")
def chat_agente(agente: str, pregunta: dict):
    pregunta_texto = pregunta.get("pregunta", "")

    contextos = {
        "inventario": ("analista de inventarios", query_low_stock_products()),
        "logistica": ("especialista en logística", query_pending_shipments()),
        "pronosticos": ("analista de pronósticos", query_demand_forecast()),
        "ejecutivo": ("asistente ejecutivo", f"KPIs:\n{query_company_kpis()}\n\nAlertas:\n{query_alerts()}"),
    }

    rol, datos = contextos.get(agente, ("asistente", "Sin datos disponibles"))

    respuesta = llm.invoke([
        SystemMessage(content=f"Eres {rol} de RetailNova Group. Responde preguntas sobre los datos de la empresa. Si la pregunta no es sobre RetailNova, responde amablemente que solo puedes ayudar con temas de la empresa. Habla en español. Sé breve y claro."),
        HumanMessage(content=f"Datos actuales:\n{datos}\n\nPregunta del usuario: {pregunta_texto}")
    ])

    return {"status": "ok", "resultado": respuesta.content}
