from crewai import Agent, LLM
from app.config import GROQ_API_KEY
from app.tools.logistics_tools import (
    get_pending_shipments,
    get_logistics_costs,
    get_delivery_performance,
    get_suppliers_ranking,
)

llm = LLM(
    model="groq/llama-3.3-70b-versatile",
    api_key=GROQ_API_KEY,
)

logistics_agent = Agent(
    role="Especialista en Logística",
    goal="Optimizar la cadena de distribución y logística de RetailNova Group, "
         "reduciendo costos de envío y mejorando los tiempos de entrega.",
    backstory=(
        "Eres un ingeniero logístico con experiencia en cadenas de suministro "
        "multinacionales en Latinoamérica. Conoces a fondo los transportistas, "
        "rutas y costos de la región. Tu objetivo es minimizar costos logísticos "
        "mientras se garantiza la entrega oportuna a las 300+ tiendas."
    ),
    tools=[
        get_pending_shipments,
        get_logistics_costs,
        get_delivery_performance,
        get_suppliers_ranking,
    ],
    llm=llm,
    verbose=True,
    allow_delegation=False,
    max_iter=5,
)
