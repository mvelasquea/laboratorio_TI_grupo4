import sqlite3
import os
import json

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "retailnova.db")


def _get_connection():
    return sqlite3.connect(DB_PATH)


def get_low_stock_products():
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
        return "No hay productos con stock bajo."

    data = []
    for r in results:
        data.append({
            "tienda": r[1],
            "producto": r[2],
            "sku": r[3],
            "stock_actual": r[4],
            "stock_minimo": r[5],
            "riesgo": "CRITICO" if r[4] <= r[5] else "ALTO",
        })
    return json.dumps(data, indent=2, ensure_ascii=False)


def get_pending_shipments():
    conn = _get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT e.id, e.transportista, e.origen, e.destino,
               e.estado, e.fecha_salida, e.costo_envio
        FROM envios e
        WHERE e.estado IN ('Pendiente', 'En Transito')
        ORDER BY e.fecha_salida ASC
        LIMIT 20
    """)
    results = cursor.fetchall()
    conn.close()

    if not results:
        return "No hay envíos pendientes."

    data = []
    for r in results:
        data.append({
            "envio_id": r[0],
            "transportista": r[1],
            "origen": r[2],
            "destino": r[3],
            "estado": r[4],
            "costo": r[6],
        })
    return json.dumps(data, indent=2, ensure_ascii=False)


def get_demand_forecast():
    conn = _get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT p.nombre, p.categoria, SUM(v.cantidad) as total_vendido,
               AVG(v.cantidad) as promedio_diario
        FROM ventas v
        JOIN productos p ON v.producto_id = p.id
        WHERE v.fecha >= date('now', '-30 days')
        GROUP BY p.id
        ORDER BY total_vendido DESC
        LIMIT 10
    """)
    results = cursor.fetchall()
    conn.close()

    if not results:
        return "No hay datos de pronóstico."

    data = []
    for r in results:
        data.append({
            "producto": r[0],
            "categoria": r[1],
            "total_vendido_30d": r[2],
            "promedio_diario": round(r[3], 2),
        })
    return json.dumps(data, indent=2, ensure_ascii=False)


def get_company_kpis():
    conn = _get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT AVG(tasa_rotura_stock), AVG(tiempo_promedio_entrega),
               AVG(costo_logistica), AVG(precision_pronostico),
               SUM(ventas_totales), SUM(numero_ordenes)
        FROM kpis WHERE mes = 11 AND anio = 2024
    """)
    r = cursor.fetchone()
    conn.close()

    return json.dumps({
        "tasa_rotura_stock": round(r[0], 2) if r[0] else 0,
        "tiempo_entrega_dias": round(r[1], 1) if r[1] else 0,
        "costo_logistico": round(r[2], 2) if r[2] else 0,
        "precision_pronostico": round(r[3], 1) if r[3] else 0,
        "ventas_totales": round(r[4], 2) if r[4] else 0,
        "total_ordenes": r[5] if r[5] else 0,
    }, indent=2, ensure_ascii=False)


def get_alerts():
    conn = _get_connection()
    cursor = conn.cursor()
    alerts = []

    cursor.execute("SELECT COUNT(*) FROM inventarios WHERE stock_actual <= stock_minimo")
    low_stock = cursor.fetchone()[0]
    if low_stock > 0:
        alerts.append({"tipo": "CRITICO", "mensaje": f"{low_stock} productos con stock bajo"})

    cursor.execute("SELECT COUNT(*) FROM envios WHERE estado = 'En Transito' AND fecha_salida < date('now', '-10 days')")
    delayed = cursor.fetchone()[0]
    if delayed > 0:
        alerts.append({"tipo": "ALERTA", "mensaje": f"{delayed} envíos con retraso"})

    conn.close()
    return json.dumps(alerts if alerts else [{"tipo": "INFO", "mensaje": "No hay alertas"}], indent=2, ensure_ascii=False)
