from fastapi import APIRouter
from app.agents.crew import run_crew_analysis

router = APIRouter()


@router.post("/ejecutar")
def ejecutar_analisis():
    try:
        resultado = run_crew_analysis()
        return {"status": "ok", "resultado": str(resultado)}
    except Exception as e:
        return {"status": "error", "mensaje": str(e)}


@router.get("/estado")
def estado_sistema():
    return {
        "status": "activo",
        "agentes": ["inventario", "logística", "pronósticos", "ejecutivo"],
        "base_datos": "conectada",
    }
