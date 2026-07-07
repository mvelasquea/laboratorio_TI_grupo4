from fastapi import APIRouter
from app.tools.db_queries import (
    query_demand_forecast,
    query_forecast_accuracy,
    query_sales_trends,
    query_top_products,
)

router = APIRouter()


@router.get("/demanda")
def pronostico_demanda():
    return {"data": query_demand_forecast()}


@router.get("/precision")
def precision_pronosticos():
    return {"data": query_forecast_accuracy()}


@router.get("/tendencias")
def tendencias_ventas():
    return {"data": query_sales_trends()}


@router.get("/productos-top")
def productos_top():
    return {"data": query_top_products()}
