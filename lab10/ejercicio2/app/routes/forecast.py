from fastapi import APIRouter
from app.tools.forecast_tools import (
    _get_demand_forecast_fn,
    _get_forecast_accuracy_fn,
    _get_sales_trends_fn,
    _get_top_products_fn,
)

router = APIRouter()


@router.get("/demanda")
def pronostico_demanda():
    return {"data": _get_demand_forecast_fn()}


@router.get("/precision")
def precision_pronosticos():
    return {"data": _get_forecast_accuracy_fn()}


@router.get("/tendencias")
def tendencias_ventas():
    return {"data": _get_sales_trends_fn()}


@router.get("/productos-top")
def productos_top():
    return {"data": _get_top_products_fn()}
