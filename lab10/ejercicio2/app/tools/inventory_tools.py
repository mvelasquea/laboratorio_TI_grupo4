from crewai import Tool
import sqlite3
import os
import json

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "retailnova.db")


def _get_connection():
    return sqlite3.connect(DB_PATH)


def _get_low_stock_products_fn():
    conn = _get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT i.id, t.nombre as tienda, p.nombre as producto, p.sku,
               i.stock_actual, i.stock_minimo, p.precio_venta
        FROM inventarios i
        JOIN tiendas t ON i.tienda_id = t.id
        JOIN productos p ON i.producto_id = p.id
        WHERE i.stock_actual <= i.stock_minimo * 1.2
        ORDER BY (i.stock_actual * 1.0 / i.stock_minimo) ASC
        LIMIT 20
    """)
    results = cursor.fetchall()
    conn.close()

    if not results:
        return "No hay productos con stock bajo en este momento."

    data = []
    for r in results:
        data.append({
            "id": r[0],
            "tienda": r[1],
            "producto": r[2],
            "sku": r[3],
            "stock_actual": r[4],
            "stock_minimo": r[5],
            "precio_venta": r[6],
            "riesgo": "CRITICO" if r[4] <= r[5] else "ALTO",
        })
    return json.dumps(data, indent=2, ensure_ascii=False)


def _get_inventory_by_store_fn(tienda_id: int = 1):
    conn = _get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT p.nombre, p.sku, i.stock_actual, i.stock_minimo, i.stock_maximo,
               p.precio_venta, i.fecha_ultima_reposicion
        FROM inventarios i
        JOIN productos p ON i.producto_id = p.id
        WHERE i.tienda_id = ?
        ORDER BY i.stock_actual ASC
    """, (tienda_id,))
    results = cursor.fetchall()
    conn.close()

    if not results:
        return f"No se encontraron inventarios para la tienda {tienda_id}."

    data = []
    for r in results:
        data.append({
            "producto": r[0],
            "sku": r[1],
            "stock_actual": r[2],
            "stock_minimo": r[3],
            "stock_maximo": r[4],
            "precio_venta": r[5],
            "ultima_reposicion": r[6],
        })
    return json.dumps(data, indent=2, ensure_ascii=False)


def _calculate_reorder_point_fn(producto_id: int = 1):
    conn = _get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT AVG(cantidad) FROM ventas
        WHERE producto_id = ? AND fecha >= date('now', '-30 days')
    """, (producto_id,))
    avg_sales = cursor.fetchone()[0] or 0

    cursor.execute("""
        SELECT AVG(tiempo_entrega_dias) FROM proveedores p
        JOIN productos pr ON pr.proveedor_id = p.id
        WHERE pr.id = ?
    """, (producto_id,))
    lead_time = cursor.fetchone()[0] or 7

    reorder_point = int(avg_sales * lead_time * 1.2)

    cursor.execute("SELECT nombre FROM productos WHERE id = ?", (producto_id,))
    product_name = cursor.fetchone()
    conn.close()

    return json.dumps({
        "producto_id": producto_id,
        "nombre": product_name[0] if product_name else "Desconocido",
        "promedio_ventas_diarias": round(avg_sales, 2),
        "tiempo_entrega_dias": lead_time,
        "punto_reorden": reorder_point,
    }, indent=2, ensure_ascii=False)


def _get_stock_movements_fn():
    conn = _get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT t.nombre, COUNT(*) as total_ventas, SUM(v.cantidad) as unidades_vendidas,
               SUM(v.total) as monto_total
        FROM ventas v
        JOIN tiendas t ON v.tienda_id = t.id
        WHERE v.fecha >= date('now', '-7 days')
        GROUP BY t.nombre
        ORDER BY monto_total DESC
    """)
    results = cursor.fetchall()
    conn.close()

    data = []
    for r in results:
        data.append({
            "tienda": r[0],
            "total_ventas": r[1],
            "unidades_vendidas": r[2],
            "monto_total": round(r[3], 2),
        })
    return json.dumps(data, indent=2, ensure_ascii=False)


get_low_stock_products = Tool(
    name="get_low_stock_products",
    description="Obtiene productos con stock bajo o en riesgo de rotura. No necesita parámetros.",
    func=_get_low_stock_products_fn,
)

get_inventory_by_store = Tool(
    name="get_inventory_by_store",
    description="Obtiene el inventario completo de una tienda específica. Parámetro: tienda_id (int).",
    func=_get_inventory_by_store_fn,
)

calculate_reorder_point = Tool(
    name="calculate_reorder_point",
    description="Calcula el punto de reorden óptimo para un producto. Parámetro: producto_id (int).",
    func=_calculate_reorder_point_fn,
)

get_stock_movements = Tool(
    name="get_stock_movements",
    description="Obtiene los movimientos de stock de las tiendas en los últimos 7 días. No necesita parámetros.",
    func=_get_stock_movements_fn,
)
