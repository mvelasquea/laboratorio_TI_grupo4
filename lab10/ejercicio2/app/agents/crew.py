from crewai import Crew, Process, Task
from app.agents.agents import analista_operaciones, agente_ejecutivo


def run_crew_analysis():
    tarea_analisis = Task(
        description=(
            "Revisa el estado de inventarios, envíos pendientes, costos logísticos "
            "y KPIs de RetailNova Group. Identifica los problemas más urgentes."
        ),
        expected_output="Lista de problemas críticos encontrados y datos relevantes.",
        agent=analista_operaciones,
    )

    tarea_resumen = Task(
        description=(
            "Con base en el análisis anterior, genera un resumen ejecutivo "
            "de 5 líneas con las acciones recomendadas."
        ),
        expected_output="Resumen ejecutivo breve con recomendaciones.",
        agent=agente_ejecutivo,
    )

    crew = Crew(
        agents=[analista_operaciones, agente_ejecutivo],
        tasks=[tarea_analisis, tarea_resumen],
        process=Process.sequential,
        verbose=True,
    )

    result = crew.kickoff()
    return result
