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
        SystemMessage(content="Eres un analista de inventarios de RetailNova. Resume brevemente estos productos con stock bajo."),
        HumanMessage(content=f"Datos:\n{datos}")
    ])
    return {"status": "ok", "resultado": respuesta.content}


@router.post("/logistica")
def ejecutar_logistica():
    datos = query_pending_shipments()
    respuesta = llm.invoke([
        SystemMessage(content="Eres un especialista en logística de RetailNova. Resume brevemente estos envíos pendientes."),
        HumanMessage(content=f"Datos:\n{datos}")
    ])
    return {"status": "ok", "resultado": respuesta.content}


@router.post("/pronosticos")
def ejecutar_pronosticos():
    datos = query_demand_forecast()
    respuesta = llm.invoke([
        SystemMessage(content="Eres un analista de pronósticos de RetailNova. Resume brevemente estos datos de demanda."),
        HumanMessage(content=f"Datos:\n{datos}")
    ])
    return {"status": "ok", "resultado": respuesta.content}


@router.post("/ejecutivo")
def ejecutar_ejecutivo():
    kpis = query_company_kpis()
    alertas = query_alerts()
    respuesta = llm.invoke([
        SystemMessage(content="Eres un asistente ejecutivo de RetailNova. Resume brevemente estos KPIs y alertas."),
        HumanMessage(content=f"KPIs:\n{kpis}\n\nAlertas:\n{alertas}")
    ])
    return {"status": "ok", "resultado": respuesta.content}


@router.post("/chat/{agente}")
def chat_agente(agente: str, body: dict):
    pregunta = body.get("pregunta", "")

    if agente == "inventario":
        datos = query_low_stock_products()
        rol = "analista de inventarios de RetailNova Group"
    elif agente == "logistica":
        datos = query_pending_shipments()
        rol = "especialista en logística de RetailNova Group"
    elif agente == "pronosticos":
        datos = query_demand_forecast()
        rol = "analista de pronósticos de RetailNova Group"
    elif agente == "ejecutivo":
        datos = f"KPIs:\n{query_company_kpis()}\n\nAlertas:\n{query_alerts()}"
        rol = "asistente ejecutivo de RetailNova Group"
    else:
        return {"status": "error", "mensaje": "Agente no válido"}

    respuesta = llm.invoke([
        SystemMessage(content=f"Eres {rol}. Responde ÚNICAMENTE lo que el usuario pregunta, usando los datos que te doy como contexto. Si la pregunta no es sobre RetailNova, di que solo puedes ayudar con temas de la empresa. Sé breve y responde solo lo que te preguntan."),
        HumanMessage(content=f"CONTEXTO (datos actuales de la empresa):\n{datos}\n\nPREGUNTA DEL USUARIO: {pregunta}")
    ])

    return {"status": "ok", "resultado": respuesta.content}
