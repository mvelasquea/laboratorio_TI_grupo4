from crewai import Agent, LLM
from app.config import GROQ_API_KEY
from app.tools.inventory_tools import (
    get_low_stock_products,
    get_inventory_by_store,
    calculate_reorder_point,
    get_stock_movements,
)

llm = LLM(
    model="groq/llama-3.3-70b-versatile",
    api_key=GROQ_API_KEY,
)

inventory_agent = Agent(
    role="Analista de Inventarios",
    goal="Monitorear y optimizar los niveles de inventario de RetailNova Group, "
         "identificando productos con bajo stock, excesos y oportunidades de reabastecimiento.",
    backstory=(
        "Eres un experto en gestión de inventarios con 10 años de experiencia "
        "en cadenas de suministro retail. Tu especialidad es detectar roturas de stock "
        "antes de que ocurran y optimizar los niveles de inventario para minimizar "
        "costos de almacenamiento mientras se mantiene la disponibilidad de productos."
    ),
    tools=[
        get_low_stock_products,
        get_inventory_by_store,
        calculate_reorder_point,
        get_stock_movements,
    ],
    llm=llm,
    verbose=True,
    allow_delegation=False,
    max_iter=5,
)
