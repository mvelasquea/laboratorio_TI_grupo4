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
            "Revisa stock bajo y calcula puntos de reorden de RetailNova.",
            "Lista de productos críticos y recomendaciones.",
        )
        return {"status": "ok", "resultado": str(resultado)}
    except Exception as e:
        return {"status": "error", "mensaje": str(e)}


@router.post("/logistica")
def ejecutar_logistica():
    try:
        resultado = _run_agent(
            logistics_agent,
            "Revisa envíos pendientes y costos logísticos de RetailNova.",
            "Estado de logística y costos.",
        )
        return {"status": "ok", "resultado": str(resultado)}
    except Exception as e:
        return {"status": "error", "mensaje": str(e)}


@router.post("/pronosticos")
def ejecutar_pronosticos():
    try:
        resultado = _run_agent(
            forecast_agent,
            "Evalúa demanda y precisión de pronósticos de RetailNova.",
            "Análisis de pronósticos.",
        )
        return {"status": "ok", "resultado": str(resultado)}
    except Exception as e:
        return {"status": "error", "mensaje": str(e)}


@router.post("/ejecutivo")
def ejecutar_ejecutivo():
    try:
        resultado = _run_agent(
            executive_agent,
            "Genera resumen ejecutivo con KPIs y alertas de RetailNova.",
            "Resumen ejecutivo.",
        )
        return {"status": "ok", "resultado": str(resultado)}
    except Exception as e:
        return {"status": "error", "mensaje": str(e)}
