from crewai import Agent, LLM
from app.config import GROQ_API_KEY
from app.tools.forecast_tools import (
    get_demand_forecast,
    get_forecast_accuracy,
    get_sales_trends,
    get_top_products,
)

llm = LLM(
    model="groq/llama-3.3-70b-versatile",
    api_key=GROQ_API_KEY,
)

forecast_agent = Agent(
    role="Analista de Pronósticos",
    goal="Predecir la demanda futura de productos con alta precisión, "
         "identificando tendencias de venta y patrones estacionales.",
    backstory=(
        "Eres un data scientist especializado en pronósticos de demanda retail. "
        "Dominas técnicas de series temporales y machine learning. Tu objetivo "
        "es mejorar la precisión de los pronósticos para reducir roturas de stock "
        "y excesos de inventario en las 300+ tiendas de RetailNova Group."
    ),
    tools=[
        get_demand_forecast,
        get_forecast_accuracy,
        get_sales_trends,
        get_top_products,
    ],
    llm=llm,
    verbose=True,
    allow_delegation=False,
    max_iter=5,
)
