from fastapi import APIRouter
from app.tools.executive_tools import (
    get_company_kpis,
    get_store_performance,
    get_financial_summary,
    get_alerts,
)

router = APIRouter()


@router.get("/kpis")
def kpis_empresa():
    return {"data": get_company_kpis()}


@router.get("/tiendas")
def rendimiento_tiendas():
    return {"data": get_store_performance()}


@router.get("/resumen-financiero")
def resumen_financiero():
    return {"data": get_financial_summary()}


@router.get("/alertas")
def alertas_criticas():
    return {"data": get_alerts()}
