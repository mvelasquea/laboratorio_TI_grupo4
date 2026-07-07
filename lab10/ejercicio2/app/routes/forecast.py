from fastapi import APIRouter
from app.tools.forecast_tools import (
    get_demand_forecast,
    get_forecast_accuracy,
    get_sales_trends,
    get_top_products,
)

router = APIRouter()


@router.get("/demanda")
def pronostico_demanda():
    return {"data": get_demand_forecast()}


@router.get("/precision")
def precision_pronosticos():
    return {"data": get_forecast_accuracy()}


@router.get("/tendencias")
def tendencias_ventas():
    return {"data": get_sales_trends()}


@router.get("/productos-top")
def productos_top():
    return {"data": get_top_products()}
