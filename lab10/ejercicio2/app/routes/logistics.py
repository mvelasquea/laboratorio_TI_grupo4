from fastapi import APIRouter
from app.tools.logistics_tools import (
    get_pending_shipments,
    get_logistics_costs,
    get_delivery_performance,
    get_suppliers_ranking,
)

router = APIRouter()


@router.get("/pendientes")
def envios_pendientes():
    return {"data": get_pending_shipments()}


@router.get("/costos")
def costos_logisticos():
    return {"data": get_logistics_costs()}


@router.get("/rendimiento")
def rendimiento_entregas():
    return {"data": get_delivery_performance()}


@router.get("/proveedores")
def ranking_proveedores():
    return {"data": get_suppliers_ranking()}
