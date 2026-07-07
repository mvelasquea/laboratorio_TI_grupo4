from crewai import Crew, Process, Task
from app.agents.agents import (
    inventory_agent,
    logistics_agent,
    forecast_agent,
    executive_agent,
)


def run_crew_analysis():
    tarea_inventario = Task(
        description="Revisa stock bajo y calcula puntos de reorden.",
        expected_output="Lista de productos críticos.",
        agent=inventory_agent,
    )

    tarea_logistica = Task(
        description="Revisa envíos pendientes y costos logísticos.",
        expected_output="Estado de logística.",
        agent=logistics_agent,
    )

    tarea_pronostico = Task(
        description="Evalúa demanda y precisión de pronósticos.",
        expected_output="Análisis de pronósticos.",
        agent=forecast_agent,
    )

    tarea_ejecutivo = Task(
        description="Genera resumen ejecutivo con KPIs y alertas.",
        expected_output="Resumen ejecutivo.",
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
