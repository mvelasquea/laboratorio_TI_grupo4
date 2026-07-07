from crewai import Tool
import sqlite3
import os
import json

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "retailnova.db")


def _get_connection():
    return sqlite3.connect(DB_PATH)


def _get_pending_shipments_fn():
    conn = _get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT e.id, o.id as orden_id, e.transportista, e.origen, e.destino,
               e.estado, e.fecha_salida, e.costo_envio,
               t.nombre as tienda_destino
        FROM envios e
        JOIN ordenes o ON e.orden_id = o.id
        JOIN tiendas t ON o.tienda_id = t.id
        WHERE e.estado IN ('Pendiente', 'En Transito')
        ORDER BY e.fecha_salida ASC
        LIMIT 20
    """)
    results = cursor.fetchall()
    conn.close()

    if not results:
        return "No hay envíos pendientes o en tránsito."

    data = []
    for r in results:
        data.append({
            "envio_id": r[0],
            "orden_id": r[1],
            "transportista": r[2],
            "origen": r[3],
            "destino": r[4],
            "estado": r[5],
            "fecha_salida": r[6],
            "costo_envio": r[7],
            "tienda": r[8],
        })
    return json.dumps(data, indent=2, ensure_ascii=False)


def _get_logistics_costs_fn():
    conn = _get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT t.nombre, SUM(e.costo_envio) as total_costos,
               COUNT(e.id) as total_envios,
               AVG(e.costo_envio) as costo_promedio
        FROM envios e
        JOIN ordenes o ON e.orden_id = o.id
        JOIN tiendas t ON o.tienda_id = t.id
        WHERE e.fecha_salida >= date('now', '-30 days')
        GROUP BY t.nombre
        ORDER BY total_costos DESC
    """)
    results = cursor.fetchall()
    conn.close()

    data = []
    for r in results:
        data.append({
            "tienda": r[0],
            "costo_total": round(r[1], 2),
            "total_envios": r[2],
            "costo_promedio": round(r[3], 2),
        })
    return json.dumps(data, indent=2, ensure_ascii=False)


def _get_delivery_performance_fn():
    conn = _get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT e.transportista,
               COUNT(*) as total_envios,
               SUM(CASE WHEN e.estado = 'Entregado' THEN 1 ELSE 0 END) as entregados,
               AVG(CASE WHEN e.fecha_llegada IS NOT NULL
                   THEN julianday(e.fecha_llegada) - julianday(e.fecha_salida)
                   ELSE NULL END) as dias_promedio
        FROM envios e
        WHERE e.fecha_salida >= date('now', '-60 days')
        GROUP BY e.transportista
        ORDER BY entregados DESC
    """)
    results = cursor.fetchall()
    conn.close()

    data = []
    for r in results:
        tasa = (r[2] / r[1] * 100) if r[1] > 0 else 0
        data.append({
            "transportista": r[0],
            "total_envios": r[1],
            "entregados": r[2],
            "tasa_entrega": round(tasa, 1),
            "dias_promedio": round(r[3], 1) if r[3] else None,
        })
    return json.dumps(data, indent=2, ensure_ascii=False)


def _get_suppliers_ranking_fn():
    conn = _get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT p.nombre, p.pais, p.tiempo_entrega_dias, p.confiabilidad_score,
               COUNT(o.id) as total_ordenes,
               SUM(o.total) as monto_total
        FROM proveedores p
        LEFT JOIN ordenes o ON o.proveedor_id = p.id
        GROUP BY p.id
        ORDER BY p.confiabilidad_score DESC
    """)
    results = cursor.fetchall()
    conn.close()

    data = []
    for r in results:
        data.append({
            "proveedor": r[0],
            "pais": r[1],
            "tiempo_entrega": r[2],
            "confiabilidad": r[3],
            "total_ordenes": r[4],
            "monto_total": round(r[5], 2) if r[5] else 0,
        })
    return json.dumps(data, indent=2, ensure_ascii=False)


get_pending_shipments = Tool(
    name="get_pending_shipments",
    description="Obtiene envíos pendientes y en tránsito. No necesita parámetros.",
    func=_get_pending_shipments_fn,
)

get_logistics_costs = Tool(
    name="get_logistics_costs",
    description="Obtiene costos logísticos por tienda de los últimos 30 días. No necesita parámetros.",
    func=_get_logistics_costs_fn,
)

get_delivery_performance = Tool(
    name="get_delivery_performance",
    description="Obtiene rendimiento de entrega por transportista. No necesita parámetros.",
    func=_get_delivery_performance_fn,
)

get_suppliers_ranking = Tool(
    name="get_suppliers_ranking",
    description="Obtiene ranking de proveedores por confiabilidad. No necesita parámetros.",
    func=_get_suppliers_ranking_fn,
)
