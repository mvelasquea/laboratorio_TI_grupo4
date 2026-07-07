from fastapi import APIRouter
from app.tools.executive_tools import (
    _get_company_kpis_fn,
    _get_store_performance_fn,
    _get_financial_summary_fn,
    _get_alerts_fn,
)

router = APIRouter()


@router.get("/kpis")
def kpis_empresa():
    return {"data": _get_company_kpis_fn()}


@router.get("/tiendas")
def rendimiento_tiendas():
    return {"data": _get_store_performance_fn()}


@router.get("/resumen-financiero")
def resumen_financiero():
    return {"data": _get_financial_summary_fn()}


@router.get("/alertas")
def alertas_criticas():
    return {"data": _get_alerts_fn()}
