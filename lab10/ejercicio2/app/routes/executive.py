from fastapi import APIRouter
from app.tools.db_queries import (
    query_company_kpis,
    query_store_performance,
    query_financial_summary,
    query_alerts,
)

router = APIRouter()


@router.get("/kpis")
def kpis_empresa():
    return {"data": query_company_kpis()}


@router.get("/tiendas")
def rendimiento_tiendas():
    return {"data": query_store_performance()}


@router.get("/resumen-financiero")
def resumen_financiero():
    return {"data": query_financial_summary()}


@router.get("/alertas")
def alertas_criticas():
    return {"data": query_alerts()}
