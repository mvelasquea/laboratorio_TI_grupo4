const API_BASE = '';
let agenteActual = null;

// Guardar y cargar chats del localStorage
function guardarChat(agente, mensajes) {
    localStorage.setItem(`chat_${agente}`, JSON.stringify(mensajes));
}

function cargarChat(agente) {
    const datos = localStorage.getItem(`chat_${agente}`);
    return datos ? JSON.parse(datos) : [];
}

function mostrarPanel(id) {
    document.querySelectorAll('.panel').forEach(p => p.classList.add('oculto'));
    document.getElementById(id).classList.remove('oculto');
}

function mostrarCargando(containerId) {
    document.getElementById(containerId).innerHTML = '<div class="cargando">Cargando datos...</div>';
}

// Funciones de carga de datos
async function cargarKPIs() {
    mostrarPanel('panel-kpis');
    mostrarCargando('kpi-container');
    try {
        const res = await fetch(`${API_BASE}/api/executive/kpis`);
        const data = await res.json();
        const kpis = JSON.parse(data.data);
        let html = '';
        const labels = {
            tasa_rotura_stock: 'Rotura Stock',
            tiempo_entrega: 'Entrega (días)',
            costo_logistico: 'Costo Logístico',
            precision_pronostico: 'Precisión Pronóstico',
            ventas_totales: 'Ventas Totales',
            total_ordenes: 'Órdenes Totales',
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
            html += `<tr><td>${item.envio_id}</td><td>${item.transportista}</td><td>${item.origen}</td><td>${item.destino}</td><td><span class="badge ${badge}">${item.estado}</span></td><td>$${item.costo}</td></tr>`;
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
        let html = '<table class="tabla"><thead><tr><th>Producto</th><th>Vendido (30d)</th><th>Promedio/Día</th></tr></thead><tbody>';
        items.forEach(item => {
            html += `<tr><td>${item.producto}</td><td>${item.total_vendido}</td><td>${item.promedio_diario}</td></tr>`;
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

// Funciones del chat
function abrirChat(agente) {
    agenteActual = agente;
    const nombres = {
        inventario: '📦 Agente de Inventario',
        logistica: '🚚 Agente de Logística',
        pronosticos: '📈 Agente de Pronósticos',
        ejecutivo: '👔 Agente Ejecutivo'
    };
    document.getElementById('chat-titulo').textContent = nombres[agente];

    document.querySelectorAll('.btn-agente').forEach(btn => btn.classList.remove('activo'));
    document.querySelector(`[data-agente="${agente}"]`).classList.add('activo');

    mostrarPanel('panel-chat');
    renderizarChat();
}

function renderizarChat() {
    const mensajes = cargarChat(agenteActual);
    const container = document.getElementById('chat-mensajes');
    container.innerHTML = '';

    if (mensajes.length === 0) {
        container.innerHTML = '<div class="chat-vacio">Escribe una pregunta sobre la cadena de suministro de RetailNova Group</div>';
        return;
    }

    mensajes.forEach(msg => {
        const div = document.createElement('div');
        div.className = `chat-msg chat-${msg.tipo}`;
        div.innerHTML = `<div class="msg-contenido">${msg.texto}</div>`;
        container.appendChild(div);
    });

    container.scrollTop = container.scrollHeight;
}

function agregarMensaje(tipo, texto) {
    const mensajes = cargarChat(agenteActual);
    mensajes.push({ tipo, texto, timestamp: Date.now() });
    guardarChat(agenteActual, mensajes);
    renderizarChat();
}

async function enviarMensaje() {
    const input = document.getElementById('chat-input');
    const texto = input.value.trim();
    if (!texto || !agenteActual) return;

    input.value = '';
    agregarMensaje('usuario', texto);

    const msgDiv = document.createElement('div');
    msgDiv.className = 'chat-msg chat-asistente';
    msgDiv.innerHTML = '<div class="msg-contenido cargando-chat">Pensando...</div>';
    document.getElementById('chat-mensajes').appendChild(msgDiv);

    try {
        const res = await fetch(`${API_BASE}/api/agents/${agenteActual}`, { method: 'POST' });
        const data = await res.json();
        const respuesta = data.status === 'ok' ? data.resultado : 'Error: ' + data.mensaje;

        msgDiv.querySelector('.msg-contenido').textContent = respuesta;
        const mensajes = cargarChat(agenteActual);
        mensajes.push({ tipo: 'asistente', texto: respuesta, timestamp: Date.now() });
        guardarChat(agenteActual, mensajes);
    } catch (e) {
        msgDiv.querySelector('.msg-contenido').textContent = 'Error al conectar con el agente.';
    }

    document.getElementById('chat-mensajes').scrollTop = document.getElementById('chat-mensajes').scrollHeight;
}

function limpiarChat() {
    if (agenteActual && confirm('¿Limpiar el historial de este chat?')) {
        localStorage.removeItem(`chat_${agenteActual}`);
        renderizarChat();
    }
}

// Cargar KPIs al inicio
document.addEventListener('DOMContentLoaded', cargarKPIs);
