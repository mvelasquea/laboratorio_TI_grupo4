from crewai import Crew, Process, Task
from app.agents.inventory_agent import inventory_agent
from app.agents.logistics_agent import logistics_agent
from app.agents.forecast_agent import forecast_agent
from app.agents.executive_agent import executive_agent


def create_inventory_task():
    return Task(
        description=(
            "Analiza el estado actual del inventario de RetailNova Group. "
            "Identifica productos con stock bajo, calcula puntos de reorden "
            "y recomienda acciones de reabastecimiento. "
            "Enfócate en prevenir roturas de stock."
        ),
        expected_output=(
            "Un reporte detallado con: 1) Lista de productos críticos, "
            "2) Puntos de reorden calculados, 3) Recomendaciones de compra."
        ),
        agent=inventory_agent,
    )


def create_logistics_task():
    return Task(
        description=(
            "Analiza la operación logística de RetailNova Group. "
            "Revisa envíos pendientes, costos por transportista y "
            "tiempos de entrega. Identifica oportunidades de optimización."
        ),
        expected_output=(
            "Un reporte con: 1) Estado de envíos pendientes, "
            "2) Análisis de costos logísticos, 3) Ranking de transportistas."
        ),
        agent=logistics_agent,
    )


def create_forecast_task():
    return Task(
        description=(
            "Analiza las tendencias de venta y precisión de pronósticos "
            "de RetailNova Group. Identifica productos con mayor demanda "
            "y evalúa la precisión de predicciones anteriores."
        ),
        expected_output=(
            "Un reporte con: 1) Top productos por demanda, "
            "2) Tendencias de venta, 3) Evaluación de precisión."
        ),
        agent=forecast_agent,
    )


def create_executive_task():
    return Task(
        description=(
            "Consolida los reportes de inventario, logística y pronósticos "
            "para generar un resumen ejecutivo. Incluye KPIs principales, "
            "alertas críticas y recomendaciones estratégicas."
        ),
        expected_output=(
            "Un resumen ejecutivo con: 1) KPIs del mes, "
            "2) Alertas críticas, 3) Recomendaciones para la dirección."
        ),
        agent=executive_agent,
    )


def run_crew_analysis():
    crew = Crew(
        agents=[inventory_agent, logistics_agent, forecast_agent, executive_agent],
        tasks=[
            create_inventory_task(),
            create_logistics_task(),
            create_forecast_task(),
            create_executive_task(),
        ],
        process=Process.sequential,
        verbose=True,
    )

    result = crew.kickoff()
    return result
