const API_BASE = '';

function mostrarPanel(id) {
    document.querySelectorAll('.panel').forEach(p => p.classList.add('oculto'));
    document.getElementById(id).classList.remove('oculto');
}

function mostrarCargando(containerId) {
    document.getElementById(containerId).innerHTML = '<div class="cargando">Cargando datos...</div>';
}

async function cargarKPIs() {
    mostrarPanel('panel-kpis');
    mostrarCargando('kpi-container');
    try {
        const res = await fetch(`${API_BASE}/api/executive/kpis`);
        const data = await res.json();
        const kpis = JSON.parse(data.data);
        let html = '';
        const labels = {
            tasa_rotura_stock_promedio: 'Rotura de Stock',
            tiempo_entrega_promedio_entrega: 'Tiempo Entrega (días)',
            costo_logistica_promedio: 'Costo Logístico',
            precision_pronostico_promedio: 'Precisión Pronóstico',
            ventas_totales_mes: 'Ventas Totales',
            total_ordenes_mes: 'Órdenes Totales',
        };
        for (const [key, val] of Object.entries(kpis)) {
            html += `<div class="kpi-card"><h3>${labels[key] || key}</h3><div class="valor">${
                typeof val === 'number' ? val.toLocaleString('es-PE') : val
            }</div></div>`;
        }
        document.getElementById('kpi-container').innerHTML = html;
    } catch (e) {
        document.getElementById('kpi-container').innerHTML = '<p>Error al cargar KPIs</p>';
    }
}

async function cargarInventarios() {
    mostrarPanel('panel-inventarios');
    mostrarCargando('inventario-container');
    try {
        const res = await fetch(`${API_BASE}/api/inventory/low-stock`);
        const data = await res.json();
        const items = JSON.parse(data.data);
        let html = '<table class="tabla"><thead><tr><th>Tienda</th><th>Producto</th><th>SKU</th><th>Stock</th><th>Mínimo</th><th>Riesgo</th></tr></thead><tbody>';
        items.forEach(item => {
            const badge = item.riesgo === 'CRITICO' ? 'badge-critico' : 'badge-alerta';
            html += `<tr><td>${item.tienda}</td><td>${item.producto}</td><td>${item.sku}</td><td>${item.stock_actual}</td><td>${item.stock_minimo}</td><td><span class="badge ${badge}">${item.riesgo}</span></td></tr>`;
        });
        html += '</tbody></table>';
        document.getElementById('inventario-container').innerHTML = html;
    } catch (e) {
        document.getElementById('inventario-container').innerHTML = '<p>Error al cargar inventarios</p>';
    }
}

async function cargarLogistica() {
    mostrarPanel('panel-logistica');
    mostrarCargando('logistica-container');
    try {
        const res = await fetch(`${API_BASE}/api/logistics/pendientes`);
        const data = await res.json();
        const items = JSON.parse(data.data);
        let html = '<table class="tabla"><thead><tr><th>ID</th><th>Transportista</th><th>Origen</th><th>Destino</th><th>Estado</th><th>Costo</th></tr></thead><tbody>';
        items.forEach(item => {
            const badge = item.estado === 'En Transito' ? 'badge-alerta' : 'badge-info';
            html += `<tr><td>${item.envio_id}</td><td>${item.transportista}</td><td>${item.origen}</td><td>${item.destino}</td><td><span class="badge ${badge}">${item.estado}</span></td><td>$${item.costo_envio}</td></tr>`;
        });
        html += '</tbody></table>';
        document.getElementById('logistica-container').innerHTML = html;
    } catch (e) {
        document.getElementById('logistica-container').innerHTML = '<p>Error al cargar logística</p>';
    }
}

async function cargarPronosticos() {
    mostrarPanel('panel-pronosticos');
    mostrarCargando('pronostico-container');
    try {
        const res = await fetch(`${API_BASE}/api/forecast/demanda`);
        const data = await res.json();
        const items = JSON.parse(data.data);
        let html = '<table class="tabla"><thead><tr><th>Producto</th><th>Categoría</th><th>Vendido (30d)</th><th>Promedio/Día</th><th>Pronóstico</th></tr></thead><tbody>';
        items.forEach(item => {
            html += `<tr><td>${item.producto}</td><td>${item.categoria}</td><td>${item.total_vendido_30d}</td><td>${item.promedio_diario}</td><td>${item.pronostico_30d}</td></tr>`;
        });
        html += '</tbody></table>';
        document.getElementById('pronostico-container').innerHTML = html;
    } catch (e) {
        document.getElementById('pronostico-container').innerHTML = '<p>Error al cargar pronósticos</p>';
    }
}

async function cargarAlertas() {
    mostrarPanel('panel-alertas');
    mostrarCargando('alerta-container');
    try {
        const res = await fetch(`${API_BASE}/api/executive/alertas`);
        const data = await res.json();
        const items = JSON.parse(data.data);
        let html = '';
        items.forEach(item => {
            const badge = item.tipo === 'CRITICO' ? 'badge-critico' : item.tipo === 'ALERTA' ? 'badge-alerta' : 'badge-ok';
            html += `<div style="margin-bottom:10px;"><span class="badge ${badge}">${item.tipo}</span> ${item.mensaje}</div>`;
        });
        document.getElementById('alerta-container').innerHTML = html;
    } catch (e) {
        document.getElementById('alerta-container').innerHTML = '<p>Error al cargar alertas</p>';
    }
}

async function ejecutarAnalisis() {
    mostrarPanel('panel-resultado');
    document.getElementById('resultado-container').innerHTML = '<div class="cargando">Ejecutando agentes IA... Esto puede tomar unos segundos.</div>';
    try {
        const res = await fetch(`${API_BASE}/api/analysis/ejecutar`, { method: 'POST' });
        const data = await res.json();
        if (data.status === 'ok') {
            document.getElementById('resultado-container').textContent = data.resultado;
        } else {
            document.getElementById('resultado-container').textContent = 'Error: ' + data.mensaje;
        }
    } catch (e) {
        document.getElementById('resultado-container').textContent = 'Error al ejecutar el análisis: ' + e.message;
    }
}

document.addEventListener('DOMContentLoaded', cargarKPIs);
