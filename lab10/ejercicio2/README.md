# RetailNova Group - Agentes IA para Cadena de Suministro

Sistema de agentes IA colaborativos para optimizar la cadena de suministro de RetailNova Group, corporación multinacional con más de 300 tiendas en Latinoamérica.

## Problemas que resuelve

- Ruptura de stock en tiendas
- Incremento de costos logísticos
- Retrasos en distribución
- Baja precisión de pronósticos de demanda

## Agentes IA

| Agente | Función |
|--------|---------|
| **Inventarios** | Detecta stock bajo, calcula puntos de reorden |
| **Logística** | Revisa envíos pendientes y costos |
| **Pronósticos** | Evalúa demanda y precisión de predicciones |
| **Ejecutivo** | Consolida KPIs y genera alertas |

## Tecnologías

- **Framework de agentes:** LangChain
- **Motor de LLM:** Ollama (Llama 3.2) - Local
- **Servidor:** FastAPI
- **Base de datos:** SQLite
- **Dashboard:** HTML/CSS/JS con chat interactivo

## Instalación

```bash
pip install -r requirements.txt
```

## Configuración

1. Instalar Ollama: https://ollama.com
2. Descargar el modelo: `ollama pull llama3.2`
3. Crear archivo `.env`:

```
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2
DATABASE_URL=sqlite:///retailnova.db
```

## Ejecución

```bash
python run.py
```

El servidor estará disponible en `http://localhost:8000`

## Endpoints API

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/api/inventory/low-stock` | Productos con stock bajo |
| GET | `/api/inventory/store/{id}` | Inventario por tienda |
| GET | `/api/logistics/pendientes` | Envíos pendientes |
| GET | `/api/logistics/costos` | Costos logísticos |
| GET | `/api/forecast/demanda` | Pronóstico de demanda |
| GET | `/api/executive/kpis` | KPIs de la empresa |
| GET | `/api/executive/alertas` | Alertas críticas |
| POST | `/api/agents/chat/{agente}` | Chat interactivo con agente |

## Dashboard

Acceder a `http://localhost:8000` para ver el panel de control con chat interactivo persistente.

## Estructura del proyecto

```
ejercicio2/
├── app/
│   ├── agents/        # Orquestador de agentes
│   ├── tools/         # Consultas a base de datos
│   ├── models/        # Población de BD
│   ├── routes/        # Endpoints API
│   ├── dashboard/     # Frontend con chat
│   ├── config.py      # Configuración Ollama
│   └── main.py        # Servidor FastAPI
├── retailnova.db      # Base de datos SQLite
├── requirements.txt   # Dependencias
└── run.py             # Punto de entrada
```
