from crewai import Crew, Process, Task
from app.agents.agents import (
    inventory_agent,
    logistics_agent,
    forecast_agent,
    executive_agent,
)


def run_crew_analysis():
    tarea_inventario = Task(
        description="EJECUTA UNA SOLA VEZ la herramienta productos_stock_bajo. Luego resume los resultados en texto claro. No vuelvas a ejecutar la herramienta.",
        expected_output="Resumen de productos con stock bajo.",
        agent=inventory_agent,
    )

    tarea_logistica = Task(
        description="EJECUTA UNA SOLA VEZ la herramienta envios_pendientes. Luego resume los resultados en texto claro. No vuelvas a ejecutar la herramienta.",
        expected_output="Resumen de envíos pendientes.",
        agent=logistics_agent,
    )

    tarea_pronostico = Task(
        description="EJECUTA UNA SOLA VEZ la herramienta pronostico_demanda. Luego resume los resultados en texto claro. No vuelvas a ejecutar la herramienta.",
        expected_output="Resumen de pronósticos de demanda.",
        agent=forecast_agent,
    )

    tarea_ejecutivo = Task(
        description="EJECUTA UNA SOLA VEZ la herramienta kpis_empresa. Luego resume los resultados en texto claro. No vuelvas a ejecutar la herramienta.",
        expected_output="Resumen de KPIs ejecutivos.",
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
