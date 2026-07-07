from fastapi import APIRouter
from app.tools.inventory_tools import (
    _get_low_stock_products_fn,
    _get_inventory_by_store_fn,
    _calculate_reorder_point_fn,
    _get_stock_movements_fn,
)

router = APIRouter()


@router.get("/low-stock")
def low_stock():
    return {"data": _get_low_stock_products_fn()}


@router.get("/store/{tienda_id}")
def inventory_by_store(tienda_id: int):
    return {"data": _get_inventory_by_store_fn(tienda_id)}


@router.get("/reorder/{producto_id}")
def reorder_point(producto_id: int):
    return {"data": _calculate_reorder_point_fn(producto_id)}


@router.get("/movements")
def stock_movements():
    return {"data": _get_stock_movements_fn()}
