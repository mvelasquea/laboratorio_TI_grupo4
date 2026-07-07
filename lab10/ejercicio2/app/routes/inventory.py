from fastapi import APIRouter
from app.tools.inventory_tools import (
    get_low_stock_products,
    get_inventory_by_store,
    calculate_reorder_point,
    get_stock_movements,
)

router = APIRouter()


@router.get("/low-stock")
def low_stock():
    return {"data": get_low_stock_products()}


@router.get("/store/{tienda_id}")
def inventory_by_store(tienda_id: int):
    return {"data": get_inventory_by_store(tienda_id)}


@router.get("/reorder/{producto_id}")
def reorder_point(producto_id: int):
    return {"data": calculate_reorder_point(producto_id)}


@router.get("/movements")
def stock_movements():
    return {"data": get_stock_movements()}
