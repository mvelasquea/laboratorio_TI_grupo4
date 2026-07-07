from fastapi import APIRouter
from app.tools.db_queries import (
    query_pending_shipments,
    query_logistics_costs,
    query_delivery_performance,
    query_suppliers_ranking,
)

router = APIRouter()


@router.get("/pendientes")
def envios_pendientes():
    return {"data": query_pending_shipments()}


@router.get("/costos")
def costos_logisticos():
    return {"data": query_logistics_costs()}


@router.get("/rendimiento")
def rendimiento_entregas():
    return {"data": query_delivery_performance()}


@router.get("/proveedores")
def ranking_proveedores():
    return {"data": query_suppliers_ranking()}
