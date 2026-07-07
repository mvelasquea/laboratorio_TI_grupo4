from crewai import Crew, Process, Task
from app.agents.agents import (
    inventory_agent,
    logistics_agent,
    forecast_agent,
    executive_agent,
)


def run_crew_analysis():
    tarea_inventario = Task(
        description="Usa la herramienta productos_stock_bajo para obtener la lista de productos con stock bajo. Luego presenta los resultados de forma clara y concisa.",
        expected_output="Lista de productos críticos con stock bajo, tienda, SKU y nivel de riesgo.",
        agent=inventory_agent,
    )

    tarea_logistica = Task(
        description="Usa la herramienta envios_pendientes para obtener envíos pendientes y costos_logisticos para costos. Presenta un resumen claro.",
        expected_output="Resumen de envíos pendientes y costos logísticos por tienda.",
        agent=logistics_agent,
    )

    tarea_pronostico = Task(
        description="Usa la herramienta pronostico_demanda para obtener pronósticos y precision_pronosticos para evaluar exactitud. Presenta el análisis.",
        expected_output="Análisis de demanda estimada y precisión de pronósticos.",
        agent=forecast_agent,
    )

    tarea_ejecutivo = Task(
        description="Usa kpis_empresa para obtener métricas y alertas_criticas para alertas. Genera un resumen ejecutivo consolidado.",
        expected_output="Resumen ejecutivo con KPIs principales y alertas críticas.",
        agent=executive_agent,
    )

    crew = Crew(
        agents=[inventory_agent, logistics_agent, forecast_agent, executive_agent],
        tasks=[tarea_inventario, tarea_logistica, tarea_pronostico, tarea_ejecutivo],
        process=Process.sequential,
        verbose=True,
    )

    result = crew.kickoff()
    return result
