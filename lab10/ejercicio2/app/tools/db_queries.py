import sqlite3
import os
import json

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "retailnova.db")


def _get_connection():
    return sqlite3.connect(DB_PATH)


def _to_json(results, columns):
    data = []
    for r in results:
        data.append(dict(zip(columns, r)))
    return json.dumps(data, indent=2, ensure_ascii=False)


def query_low_stock_products():
    conn = _get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT t.nombre as tienda, p.nombre as producto, p.sku,
               i.stock_actual, i.stock_minimo,
               CASE WHEN i.stock_actual <= i.stock_minimo THEN 'CRITICO' ELSE 'ALTO' END as riesgo
        FROM inventarios i
        JOIN tiendas t ON i.tienda_id = t.id
        JOIN productos p ON i.producto_id = p.id
        WHERE i.stock_actual <= i.stock_minimo * 1.2
        ORDER BY (i.stock_actual * 1.0 / i.stock_minimo) ASC
    """)
    results = cursor.fetchall()
    conn.close()
    return _to_json(results, ["tienda", "producto", "sku", "stock_actual", "stock_minimo", "riesgo"])


def query_inventory_by_store(tienda_id):
    conn = _get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT p.nombre, p.sku, i.stock_actual, i.stock_minimo, i.stock_maximo
        FROM inventarios i
        JOIN productos p ON i.producto_id = p.id
        WHERE i.tienda_id = ?
    """, (tienda_id,))
    results = cursor.fetchall()
    conn.close()
    return _to_json(results, ["producto", "sku", "stock_actual", "stock_minimo", "stock_maximo"])


def query_reorder_point(producto_id):
    conn = _get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT AVG(cantidad) FROM ventas WHERE producto_id = ?", (producto_id,))
    avg_sales = cursor.fetchone()[0] or 0
    cursor.execute("SELECT AVG(tiempo_entrega_dias) FROM proveedores p JOIN productos pr ON pr.proveedor_id = p.id WHERE pr.id = ?", (producto_id,))
    lead_time = cursor.fetchone()[0] or 7
    conn.close()
    return json.dumps({"producto_id": producto_id, "promedio_ventas": round(avg_sales, 2), "tiempo_entrega": lead_time, "punto_reorden": int(avg_sales * lead_time * 1.2)}, indent=2)


def query_stock_movements():
    conn = _get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT t.nombre, COUNT(*) as ventas, SUM(v.cantidad) as unidades
        FROM ventas v JOIN tiendas t ON v.tienda_id = t.id
        GROUP BY t.nombre ORDER BY unidades DESC
    """)
    results = cursor.fetchall()
    conn.close()
    return _to_json(results, ["tienda", "total_ventas", "unidades_vendidas"])


def query_pending_shipments():
    conn = _get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT e.id, e.transportista, e.origen, e.destino, e.estado, e.costo_envio
        FROM envios e
        WHERE e.estado IN ('Pendiente', 'En Transito')
    """)
    results = cursor.fetchall()
    conn.close()
    return _to_json(results, ["envio_id", "transportista", "origen", "destino", "estado", "costo"])


def query_logistics_costs():
    conn = _get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT t.nombre, SUM(e.costo_envio) as total, COUNT(e.id) as envios
        FROM envios e JOIN ordenes o ON e.orden_id = o.id JOIN tiendas t ON o.tienda_id = t.id
        GROUP BY t.nombre
    """)
    results = cursor.fetchall()
    conn.close()
    return _to_json(results, ["tienda", "costo_total", "total_envios"])


def query_delivery_performance():
    conn = _get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT transportista, COUNT(*) as total,
               SUM(CASE WHEN estado = 'Entregado' THEN 1 ELSE 0 END) as entregados
        FROM envios GROUP BY transportista
    """)
    results = cursor.fetchall()
    conn.close()
    return _to_json(results, ["transportista", "total_envios", "entregados"])


def query_suppliers_ranking():
    conn = _get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT nombre, pais, confiabilidad_score FROM proveedores ORDER BY confiabilidad_score DESC")
    results = cursor.fetchall()
    conn.close()
    return _to_json(results, ["proveedor", "pais", "confiabilidad"])


def query_demand_forecast():
    conn = _get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT p.nombre, SUM(v.cantidad) as vendido, AVG(v.cantidad) as promedio
        FROM ventas v JOIN productos p ON v.producto_id = p.id
        GROUP BY p.id ORDER BY vendido DESC LIMIT 10
    """)
    results = cursor.fetchall()
    conn.close()
    return _to_json(results, ["producto", "total_vendido", "promedio_diario"])


def query_forecast_accuracy():
    conn = _get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT p.nombre, pr.demanda_estimada, pr.demanda_real, pr.precision
        FROM pronosticos pr JOIN productos p ON pr.producto_id = p.id
        WHERE pr.precision IS NOT NULL ORDER BY pr.precision ASC LIMIT 10
    """)
    results = cursor.fetchall()
    conn.close()
    return _to_json(results, ["producto", "estimada", "real", "precision"])


def query_sales_trends():
    conn = _get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT strftime('%Y-%m', fecha) as mes, SUM(total) as ventas, COUNT(*) as transacciones
        FROM ventas GROUP BY mes ORDER BY mes
    """)
    results = cursor.fetchall()
    conn.close()
    return _to_json(results, ["mes", "ventas_totales", "transacciones"])


def query_top_products():
    conn = _get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT p.nombre, SUM(v.cantidad) as unidades, SUM(v.total) as ingreso
        FROM ventas v JOIN productos p ON v.producto_id = p.id
        GROUP BY p.id ORDER BY ingreso DESC LIMIT 10
    """)
    results = cursor.fetchall()
    conn.close()
    return _to_json(results, ["producto", "unidades_vendidas", "ingreso_total"])


def query_company_kpis():
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
        "tiempo_entrega": round(r[1], 1) if r[1] else 0,
        "costo_logistico": round(r[2], 2) if r[2] else 0,
        "precision_pronostico": round(r[3], 1) if r[3] else 0,
        "ventas_totales": round(r[4], 2) if r[4] else 0,
        "total_ordenes": r[5] if r[5] else 0,
    }, indent=2)


def query_store_performance():
    conn = _get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT t.nombre, t.pais, k.ventas_totales, k.tasa_rotura_stock, k.precision_pronostico
        FROM kpis k JOIN tiendas t ON k.tienda_id = t.id WHERE k.mes = 11 AND k.anio = 2024
    """)
    results = cursor.fetchall()
    conn.close()
    return _to_json(results, ["tienda", "pais", "ventas", "rotura_stock", "precision"])


def query_financial_summary():
    conn = _get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(total), COUNT(*), AVG(total) FROM ventas")
    v = cursor.fetchone()
    cursor.execute("SELECT SUM(costo_envio) FROM envios")
    c = cursor.fetchone()
    conn.close()
    ingresos = round(v[0], 2) if v[0] else 0
    costos = round(c[0], 2) if c[0] else 0
    return json.dumps({"ingresos": ingresos, "costos_logisticos": costos, "margen": round(ingresos - costos, 2), "transacciones": v[1], "ticket_promedio": round(v[2], 2) if v[2] else 0}, indent=2)


def query_alerts():
    conn = _get_connection()
    cursor = conn.cursor()
    alerts = []
    cursor.execute("SELECT COUNT(*) FROM inventarios WHERE stock_actual <= stock_minimo")
    low = cursor.fetchone()[0]
    if low > 0:
        alerts.append({"tipo": "CRITICO", "mensaje": f"{low} productos con stock bajo"})
    cursor.execute("SELECT COUNT(*) FROM envios WHERE estado = 'En Transito' AND fecha_salida < date('now', '-10 days')")
    delayed = cursor.fetchone()[0]
    if delayed > 0:
        alerts.append({"tipo": "ALERTA", "mensaje": f"{delayed} envíos con retraso"})
    conn.close()
    return json.dumps(alerts if alerts else [{"tipo": "INFO", "mensaje": "No hay alertas"}], indent=2)
