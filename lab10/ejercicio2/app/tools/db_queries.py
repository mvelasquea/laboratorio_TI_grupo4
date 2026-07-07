import sqlite3
import os
import json

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "retailnova.db")


def _get_connection():
    return sqlite3.connect(DB_PATH)


def query_low_stock_products():
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


def query_inventory_by_store(tienda_id: int = 1):
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


def query_reorder_point(producto_id: int = 1):
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


def query_stock_movements():
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


def query_pending_shipments():
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


def query_logistics_costs():
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


def query_delivery_performance():
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


def query_suppliers_ranking():
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


def query_demand_forecast():
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


def query_forecast_accuracy():
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


def query_sales_trends():
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


def query_top_products():
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


def query_company_kpis():
    conn = _get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT AVG(tasa_rotura_stock) as avg_rotura,
               AVG(tiempo_promedio_entrega) as avg_entrega,
               AVG(costo_logistica) as avg_costo,
               AVG(precision_pronostico) as avg_precision,
               SUM(ventas_totales) as total_ventas,
               SUM(numero_ordenes) as total_ordenes
        FROM kpis
        WHERE mes = 11 AND anio = 2024
    """)
    r = cursor.fetchone()
    conn.close()

    return json.dumps({
        "tasa_rotura_stock_promedio": round(r[0], 2) if r[0] else 0,
        "tiempo_entrega_promedio_dias": round(r[1], 1) if r[1] else 0,
        "costo_logistica_promedio": round(r[2], 2) if r[2] else 0,
        "precision_pronostico_promedio": round(r[3], 1) if r[3] else 0,
        "ventas_totales_mes": round(r[4], 2) if r[4] else 0,
        "total_ordenes_mes": r[5] if r[5] else 0,
    }, indent=2, ensure_ascii=False)


def query_store_performance():
    conn = _get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT t.nombre, t.pais, t.tipo,
               k.ventas_totales, k.numero_ordenes,
               k.tasa_rotura_stock, k.precision_pronostico
        FROM kpis k
        JOIN tiendas t ON k.tienda_id = t.id
        WHERE k.mes = 11 AND k.anio = 2024
        ORDER BY k.ventas_totales DESC
        LIMIT 10
    """)
    results = cursor.fetchall()
    conn.close()

    data = []
    for r in results:
        data.append({
            "tienda": r[0],
            "pais": r[1],
            "tipo": r[2],
            "ventas_totales": round(r[3], 2),
            "total_ordenes": r[4],
            "tasa_rotura_stock": r[5],
            "precision_pronostico": r[6],
        })
    return json.dumps(data, indent=2, ensure_ascii=False)


def query_financial_summary():
    conn = _get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT SUM(total) as ingresos_totales,
               COUNT(*) as total_transacciones,
               AVG(total) as ticket_promedio
        FROM ventas
        WHERE fecha >= date('now', '-30 days')
    """)
    ventas = cursor.fetchone()

    cursor.execute("""
        SELECT SUM(costo_envio) as costos_logisticos
        FROM envios
        WHERE fecha_salida >= date('now', '-30 days')
    """)
    costos = cursor.fetchone()
    conn.close()

    ingresos = round(ventas[0], 2) if ventas[0] else 0
    costos_log = round(costos[0], 2) if costos[0] else 0
    margen = ingresos - costos_log

    return json.dumps({
        "ingresos_totales": ingresos,
        "costos_logisticos": costos_log,
        "margen_operativo": round(margen, 2),
        "total_transacciones": ventas[1],
        "ticket_promedio": round(ventas[2], 2) if ventas[2] else 0,
    }, indent=2, ensure_ascii=False)


def query_alerts():
    conn = _get_connection()
    cursor = conn.cursor()

    alerts = []

    cursor.execute("""
        SELECT COUNT(*) FROM inventarios
        WHERE stock_actual <= stock_minimo
    """)
    low_stock = cursor.fetchone()[0]
    if low_stock > 0:
        alerts.append({
            "tipo": "CRITICO",
            "mensaje": f"{low_stock} productos con stock por debajo del mínimo",
        })

    cursor.execute("""
        SELECT COUNT(*) FROM envios
        WHERE estado = 'En Transito'
        AND fecha_salida < date('now', '-10 days')
    """)
    delayed = cursor.fetchone()[0]
    if delayed > 0:
        alerts.append({
            "tipo": "ALERTA",
            "mensaje": f"{delayed} envíos con retraso mayor a 10 días",
        })

    cursor.execute("""
        SELECT COUNT(*) FROM ordenes
        WHERE estado = 'Pendiente'
        AND fecha_estimada_entrega < date('now')
    """)
    overdue = cursor.fetchone()[0]
    if overdue > 0:
        alerts.append({
            "tipo": "ALERTA",
            "mensaje": f"{overdue} órdenes con fecha de entrega vencida",
        })

    conn.close()

    if not alerts:
        alerts.append({
            "tipo": "INFO",
            "mensaje": "No hay alertas críticas en este momento",
        })

    return json.dumps(alerts, indent=2, ensure_ascii=False)
