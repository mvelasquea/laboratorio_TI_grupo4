from fastapi import APIRouter
from app.agents.agents import (
    inventory_agent,
    logistics_agent,
    forecast_agent,
    executive_agent,
)
from crewai import Crew, Process, Task

router = APIRouter()


def _run_agent(agent, description, output):
    crew = Crew(
        agents=[agent],
        tasks=[Task(description=description, expected_output=output, agent=agent)],
        process=Process.sequential,
        verbose=True,
    )
    return crew.kickoff()


@router.post("/inventario")
def ejecutar_inventario():
    try:
        resultado = _run_agent(
            inventory_agent,
            "EJECUTA UNA SOLA VEZ la herramienta productos_stock_bajo. Luego resume los resultados en texto claro. No vuelvas a ejecutar la herramienta.",
            "Resumen de productos con stock bajo.",
        )
        return {"status": "ok", "resultado": str(resultado)}
    except Exception as e:
        return {"status": "error", "mensaje": str(e)}


@router.post("/logistica")
def ejecutar_logistica():
    try:
        resultado = _run_agent(
            logistics_agent,
            "EJECUTA UNA SOLA VEZ la herramienta envios_pendientes. Luego resume los resultados en texto claro. No vuelvas a ejecutar la herramienta.",
            "Resumen de envíos pendientes.",
        )
        return {"status": "ok", "resultado": str(resultado)}
    except Exception as e:
        return {"status": "error", "mensaje": str(e)}


@router.post("/pronosticos")
def ejecutar_pronosticos():
    try:
        resultado = _run_agent(
            forecast_agent,
            "EJECUTA UNA SOLA VEZ la herramienta pronostico_demanda. Luego resume los resultados en texto claro. No vuelvas a ejecutar la herramienta.",
            "Resumen de pronósticos de demanda.",
        )
        return {"status": "ok", "resultado": str(resultado)}
    except Exception as e:
        return {"status": "error", "mensaje": str(e)}


@router.post("/ejecutivo")
def ejecutar_ejecutivo():
    try:
        resultado = _run_agent(
            executive_agent,
            "EJECUTA UNA SOLA VEZ la herramienta kpis_empresa. Luego resume los resultados en texto claro. No vuelvas a ejecutar la herramienta.",
            "Resumen de KPIs ejecutivos.",
        )
        return {"status": "ok", "resultado": str(resultado)}
    except Exception as e:
        return {"status": "error", "mensaje": str(e)}
