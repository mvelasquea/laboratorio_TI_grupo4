from fastapi import APIRouter
from app.config import OLLAMA_BASE_URL, OLLAMA_MODEL
from app.tools.db_queries import (
    query_low_stock_products,
    query_inventory_by_store,
    query_pending_shipments,
    query_logistics_costs,
    query_demand_forecast,
    query_forecast_accuracy,
    query_company_kpis,
    query_store_performance,
    query_alerts,
    query_top_products,
)
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage

router = APIRouter()

llm = ChatOllama(model=OLLAMA_MODEL, base_url=OLLAMA_BASE_URL)


def _obtener_todos_los_datos():
    return f"""PRODUCTOS CON STOCK BAJO:
{query_low_stock_products()}

INVENTARIO TIENDA 1 (Lima):
{query_inventory_by_store(1)}

INVENTARIO TIENDA 2 (Bogotá):
{query_inventory_by_store(2)}

INVENTARIO TIENDA 3 (Santiago):
{query_inventory_by_store(3)}

INVENTARIO TIENDA 4 (Online):
{query_inventory_by_store(4)}

ENVÍOS PENDIENTES:
{query_pending_shipments()}

COSTOS LOGÍSTICOS:
{query_logistics_costs()}

DEMANDA DE PRODUCTOS:
{query_demand_forecast()}

PRODUCTOS MÁS VENDIDOS:
{query_top_products()}

KPIs:
{query_company_kpis()}

RENDIMIENTO TIENDAS:
{query_store_performance()}

ALERTAS:
{query_alerts()}"""


@router.post("/inventario")
def ejecutar_inventario():
    datos = _obtener_todos_los_datos()
    respuesta = llm.invoke([
        SystemMessage(content="Eres un analista de inventarios de RetailNova Group. Usa los datos reales que te doy. Menciona nombres de productos y tiendas. Sé breve."),
        HumanMessage(content=f"DATOS:\n{datos}\n\nResume los productos con stock bajo.")
    ])
    return {"status": "ok", "resultado": respuesta.content}


@router.post("/logistica")
def ejecutar_logistica():
    datos = _obtener_todos_los_datos()
    respuesta = llm.invoke([
        SystemMessage(content="Eres un especialista en logística de RetailNova Group. Usa los datos reales que te doy. Sé breve."),
        HumanMessage(content=f"DATOS:\n{datos}\n\nResume los envíos pendientes y costos.")
    ])
    return {"status": "ok", "resultado": respuesta.content}


@router.post("/pronosticos")
def ejecutar_pronosticos():
    datos = _obtener_todos_los_datos()
    respuesta = llm.invoke([
        SystemMessage(content="Eres un analista de pronósticos de RetailNova Group. Usa los datos reales que te doy. Menciona nombres de productos. Sé breve."),
        HumanMessage(content=f"DATOS:\n{datos}\n\nResume la demanda y pronósticos.")
    ])
    return {"status": "ok", "resultado": respuesta.content}


@router.post("/ejecutivo")
def ejecutar_ejecutivo():
    datos = _obtener_todos_los_datos()
    respuesta = llm.invoke([
        SystemMessage(content="Eres un asistente ejecutivo de RetailNova Group. Usa los datos reales que te doy. Presenta KPIs y alertas. Sé breve."),
        HumanMessage(content=f"DATOS:\n{datos}\n\nGenera un resumen ejecutivo.")
    ])
    return {"status": "ok", "resultado": respuesta.content}


@router.post("/chat/{agente}")
def chat_agente(agente: str, body: dict):
    pregunta = body.get("pregunta", "")
    datos = _obtener_todos_los_datos()

    roles = {
        "inventario": "analista de inventarios",
        "logistica": "especialista en logística",
        "pronosticos": "analista de pronósticos",
        "ejecutivo": "asistente ejecutivo",
    }

    rol = roles.get(agente, "asistente de RetailNova Group")

    respuesta = llm.invoke([
        SystemMessage(content=f"""Eres {rol} de RetailNova Group.
Tienes acceso a TODA la base de datos de la empresa.
REGLAS:
- Usa los datos reales que te doy para responder.
- Menciona nombres de productos, tiendas, valores numéricos.
- Si no encuentras la información en los datos, di "no tengo esa información".
- Si la pregunta no es sobre RetailNova, di que solo puedes ayudar con temas de la empresa.
- Sé breve y responde solo lo que te preguntan."""),
        HumanMessage(content=f"BASE DE DATOS COMPLETA:\n{datos}\n\nPREGUNTA DEL USUARIO: {pregunta}")
    ])

    return {"status": "ok", "resultado": respuesta.content}
