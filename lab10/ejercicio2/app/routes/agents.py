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
        SystemMessage(content="""Eres un analista de inventarios de RetailNova Group.
REGLAS ESTRICTAS:
- Menciona los NOMBRES REALES de los productos y tiendas que aparecen en los datos.
- NO digas "Producto 1", "Producto 2". Di el nombre real como "Coca-Cola 2L" o "Laptop HP Pavilion 15".
- Sé breve y directo.
- Habla en español."""),
        HumanMessage(content=f"Datos de inventario con stock bajo:\n{datos}")
    ])
    return {"status": "ok", "resultado": respuesta.content}


@router.post("/logistica")
def ejecutar_logistica():
    datos = query_pending_shipments()
    respuesta = llm.invoke([
        SystemMessage(content="""Eres un especialista en logística de RetailNova Group.
REGLAS ESTRICTAS:
- Menciona los IDs de envío, transportistas y destinos REALES que aparecen en los datos.
- Sé breve y directo.
- Habla en español."""),
        HumanMessage(content=f"Datos de envíos pendientes:\n{datos}")
    ])
    return {"status": "ok", "resultado": respuesta.content}


@router.post("/pronosticos")
def ejecutar_pronosticos():
    datos = query_demand_forecast()
    respuesta = llm.invoke([
        SystemMessage(content="""Eres un analista de pronósticos de RetailNova Group.
REGLAS ESTRICTAS:
- Menciona los NOMBRES REALES de los productos que aparecen en los datos.
- NO digas "Producto 1". Di el nombre real como "Coca-Cola 2L" o "PlayStation 5".
- Sé breve y directo.
- Habla en español."""),
        HumanMessage(content=f"Datos de pronósticos de demanda:\n{datos}")
    ])
    return {"status": "ok", "resultado": respuesta.content}


@router.post("/ejecutivo")
def ejecutar_ejecutivo():
    kpis = query_company_kpis()
    alertas = query_alerts()
    respuesta = llm.invoke([
        SystemMessage(content="""Eres un asistente ejecutivo de RetailNova Group.
REGLAS ESTRICTAS:
- Presenta los KPIs con sus valores numéricos reales.
- Si hay alertas, menciona los detalles específicos.
- Sé breve y directo.
- Habla en español."""),
        HumanMessage(content=f"KPIs:\n{kpis}\n\nAlertas:\n{alertas}")
    ])
    return {"status": "ok", "resultado": respuesta.content}


@router.post("/chat/{agente}")
def chat_agente(agente: str, body: dict):
    pregunta = body.get("pregunta", "")

    if agente == "inventario":
        datos = query_low_stock_products()
        rol = "analista de inventarios de RetailNova Group"
        reglas = "Menciona NOMBRES REALES de productos y tiendas. NO digas 'Producto 1'. Di el nombre real."
    elif agente == "logistica":
        datos = query_pending_shipments()
        rol = "especialista en logística de RetailNova Group"
        reglas = "Menciona IDs de envío, transportistas y destinos REALES."
    elif agente == "pronosticos":
        datos = query_demand_forecast()
        rol = "analista de pronósticos de RetailNova Group"
        reglas = "Menciona NOMBRES REALES de productos. NO digas 'Producto 1'. Di el nombre real."
    elif agente == "ejecutivo":
        datos = f"KPIs:\n{query_company_kpis()}\n\nAlertas:\n{query_alerts()}"
        rol = "asistente ejecutivo de RetailNova Group"
        reglas = "Presenta valores numéricos reales. Menciona detalles específicos de alertas."
    else:
        return {"status": "error", "mensaje": "Agente no válido"}

    respuesta = llm.invoke([
        SystemMessage(content=f"""Eres {rol}.
{reglas}
Si la pregunta no es sobre RetailNova, di que solo puedes ayudar con temas de la empresa.
Sé breve, responde solo lo que te preguntan, y USA LOS DATOS REALES que te doy."""),
        HumanMessage(content=f"DATOS ACTUALES:\n{datos}\n\nPREGUNTA: {pregunta}")
    ])

    return {"status": "ok", "resultado": respuesta.content}
