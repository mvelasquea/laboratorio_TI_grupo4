from fastapi import APIRouter
from app.tools.logistics_tools import (
    _get_pending_shipments_fn,
    _get_logistics_costs_fn,
    _get_delivery_performance_fn,
    _get_suppliers_ranking_fn,
)

router = APIRouter()


@router.get("/pendientes")
def envios_pendientes():
    return {"data": _get_pending_shipments_fn()}


@router.get("/costos")
def costos_logisticos():
    return {"data": _get_logistics_costs_fn()}


@router.get("/rendimiento")
def rendimiento_entregas():
    return {"data": _get_delivery_performance_fn()}


@router.get("/proveedores")
def ranking_proveedores():
    return {"data": _get_suppliers_ranking_fn()}
