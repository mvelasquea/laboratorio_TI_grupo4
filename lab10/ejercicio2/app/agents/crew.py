from app.config import OLLAMA_BASE_URL, OLLAMA_MODEL
from app.tools.inventory_tools import get_low_stock_products
from app.tools.logistics_tools import get_pending_shipments
from app.tools.forecast_tools import get_demand_forecast
from app.tools.executive_tools import get_company_kpis
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage

llm = ChatOllama(model=OLLAMA_MODEL, base_url=OLLAMA_BASE_URL)

SYSTEM_PROMPT = """Eres un asistente de RetailNova Group, una corporación multinacional con más de 300 tiendas en Latinoamérica.

REGLAS ESTRICTAS:
1. SOLO puedes responder preguntas sobre la cadena de suministro, inventarios, logística, pronósticos y KPIs de RetailNova Group.
2. SI te preguntan sobre cualquier otro tema, responde: "Lo siento, solo puedo responder preguntas sobre la cadena de suministro de RetailNova Group."
3. NO inventes datos. Usa ÚNICAMENTE la información que te proporcionan.
4. Sé breve y conciso en tus respuestas.
5. Habla en español."""


def run_crew_analysis():
    inventario = get_low_stock_products()
    logistica = get_pending_shipments()
    pronostico = get_demand_forecast()
    kpis = get_company_kpis()

    prompt = f"""Resume estos datos de RetailNova Group de forma clara:

INVENTARIO:
{inventario}

LOGISTICA:
{logistica}

PRONOSTICOS:
{pronostico}

KPIs:
{kpis}

Genera un resumen ejecutivo breve con los puntos más importantes."""

    respuesta = llm.invoke([
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=prompt)
    ])
    return respuesta.content
