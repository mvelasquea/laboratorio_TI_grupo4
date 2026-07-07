from crewai.tools import tool
import sqlite3
import os
import json

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "retailnova.db")


def _get_connection():
    return sqlite3.connect(DB_PATH)


@tool("pronostico_demanda")
def get_demand_forecast():
    """Obtiene pronóstico de demanda basado en ventas históricas."""
    conn = _get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT p.nombre, p.categoria, SUM(v.cantidad) as total_vendido,
               AVG(v.cantidad) as promedio_diario,
               COUNT(DISTINCT v.fecha) as dias_con_venta
        FROM ventas v
        JOIN productos p ON v.producto_id = p.id
        WHERE v.fecha >= date('now', '-30 days')
        GROUP BY p.id
        ORDER BY total_vendido DESC
        LIMIT 15
    """)
    results = cursor.fetchall()
    conn.close()

    data = []
    for r in results:
        forecast = int(r[3] * 1.1)
        data.append({
            "producto": r[0],
            "categoria": r[1],
            "total_vendido_30d": r[2],
            "promedio_diario": round(r[3], 2),
            "dias_con_venta": r[4],
            "pronostico_30d": forecast,
        })
    return json.dumps(data, indent=2, ensure_ascii=False)


@tool("precision_pronosticos")
def get_forecast_accuracy():
    """Obtiene precisión de pronósticos anteriores."""
    conn = _get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT p.nombre, pr.demanda_estimada, pr.demanda_real, pr.precision,
               t.nombre as tienda
        FROM pronosticos pr
        JOIN productos p ON pr.producto_id = p.id
        JOIN tiendas t ON pr.tienda_id = t.id
        WHERE pr.precision IS NOT NULL
        ORDER BY pr.precision ASC
        LIMIT 15
    """)
    results = cursor.fetchall()
    conn.close()

    if not results:
        return "No hay datos de precisión de pronósticos disponibles."

    data = []
    for r in results:
        data.append({
            "producto": r[0],
            "demanda_estimada": r[1],
            "demanda_real": r[2],
            "precision": r[3],
            "tienda": r[4],
        })
    return json.dumps(data, indent=2, ensure_ascii=False)


@tool("tendencias_ventas")
def get_sales_trends():
    """Obtiene tendencias de ventas de los últimos 90 días."""
    conn = _get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT strftime('%Y-%m', v.fecha) as mes,
               SUM(v.total) as ventas_totales,
               COUNT(*) as numero_ventas,
               SUM(v.cantidad) as unidades
        FROM ventas v
        WHERE v.fecha >= date('now', '-90 days')
        GROUP BY mes
        ORDER BY mes ASC
    """)
    results = cursor.fetchall()
    conn.close()

    data = []
    for r in results:
        data.append({
            "mes": r[0],
            "ventas_totales": round(r[1], 2),
            "numero_ventas": r[2],
            "unidades_vendidas": r[3],
        })
    return json.dumps(data, indent=2, ensure_ascii=False)


@tool("productos_top")
def get_top_products():
    """Obtiene los 10 productos más vendidos."""
    conn = _get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT p.nombre, p.categoria, p.precio_venta,
               SUM(v.cantidad) as unidades_vendidas,
               SUM(v.total) as ingreso_total
        FROM ventas v
        JOIN productos p ON v.producto_id = p.id
        WHERE v.fecha >= date('now', '-30 days')
        GROUP BY p.id
        ORDER BY ingreso_total DESC
        LIMIT 10
    """)
    results = cursor.fetchall()
    conn.close()

    data = []
    for r in results:
        data.append({
            "producto": r[0],
            "categoria": r[1],
            "precio_venta": r[2],
            "unidades_vendidas": r[3],
            "ingreso_total": round(r[4], 2),
        })
    return json.dumps(data, indent=2, ensure_ascii=False)
