from crewai.tools import tool
import sqlite3
import os
import json

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "retailnova.db")


def _get_connection():
    return sqlite3.connect(DB_PATH)


@tool("kpis_empresa")
def get_company_kpis():
    """Obtiene KPIs principales de la empresa."""
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


@tool("rendimiento_tiendas")
def get_store_performance():
    """Obtiene rendimiento de tiendas principales."""
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


@tool("resumen_financiero")
def get_financial_summary():
    """Obtiene resumen financiero de los últimos 30 días."""
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


@tool("alertas_criticas")
def get_alerts():
    """Obtiene alertas críticas del sistema."""
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
