from app.config import OLLAMA_BASE_URL, OLLAMA_MODEL
from app.tools.db_queries import query_low_stock_products, query_pending_shipments, query_demand_forecast, query_company_kpis
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage

llm = ChatOllama(model=OLLAMA_MODEL, base_url=OLLAMA_BASE_URL)

SYSTEM_PROMPT = """Eres un asistente de RetailNova Group. SOLO responde sobre cadena de suministro. Sé breve. Habla en español."""


def run_crew_analysis():
    inventario = query_low_stock_products()
    logistica = query_pending_shipments()
    pronostico = query_demand_forecast()
    kpis = query_company_kpis()

    prompt = f"Resume estos datos de RetailNova:\n\nINVENTARIO:\n{inventario}\n\nLOGISTICA:\n{logistica}\n\nPRONOSTICOS:\n{pronostico}\n\nKPIs:\n{kpis}"

    respuesta = llm.invoke([
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=prompt)
    ])
    return respuesta.content
