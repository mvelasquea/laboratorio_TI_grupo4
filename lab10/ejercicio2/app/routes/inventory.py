from fastapi import APIRouter
from app.tools.db_queries import (
    query_low_stock_products,
    query_inventory_by_store,
    query_reorder_point,
    query_stock_movements,
)

router = APIRouter()


@router.get("/low-stock")
def low_stock():
    return {"data": query_low_stock_products()}


@router.get("/store/{tienda_id}")
def inventory_by_store(tienda_id: int):
    return {"data": query_inventory_by_store(tienda_id)}


@router.get("/reorder/{producto_id}")
def reorder_point(producto_id: int):
    return {"data": query_reorder_point(producto_id)}


@router.get("/movements")
def stock_movements():
    return {"data": query_stock_movements()}
