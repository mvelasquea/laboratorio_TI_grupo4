from crewai.tools import tool
import sqlite3
import os
import json

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "retailnova.db")


def _get_connection():
    return sqlite3.connect(DB_PATH)


@tool("productos_stock_bajo")
def get_low_stock_products():
    """Obtiene productos con stock bajo o en riesgo de rotura."""
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


@tool("inventario_por_tienda")
def get_inventory_by_store(tienda_id: int = 1):
    """Obtiene el inventario completo de una tienda específica."""
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


@tool("calcular_punto_reorden")
def calculate_reorder_point(producto_id: int = 1):
    """Calcula el punto de reorden óptimo para un producto."""
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


@tool("movimientos_stock")
def get_stock_movements():
    """Obtiene los movimientos de stock de las tiendas en los últimos 7 días."""
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
