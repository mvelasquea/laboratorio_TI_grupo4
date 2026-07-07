# RetailNova Group - Agentes IA para Cadena de Suministro

Sistema de agentes IA colaborativos para optimizar la cadena de suministro de RetailNova Group, una corporación multinacional con más de 300 tiendas en Latinoamérica.

## Problemas que resuelve

- Ruptura de stock en tiendas
- Incremento de costos logísticos
- Retrasos en distribución
- Baja precisión de pronósticos de demanda

## Agentes IA

| Agente | Función |
|--------|---------|
| **Inventarios** | Monitorea stock, detecta roturas y calcula puntos de reorden |
| **Logística** | Optimiza envíos, analiza costos y evalúa transportistas |
| **Pronósticos** | Predice demanda y evalúa precisión de predicciones |
| **Ejecutivo** | Consolida KPIs, genera alertas y recomendaciones |

## Tecnologías

- **Framework de agentes:** CrewAI
- **Motor de LLM:** Ollama (Llama 3.2)
- **Servidor:** FastAPI
- **Base de datos:** SQLite
- **Dashboard:** HTML/CSS/JS

## Instalación

```bash
pip install -r requirements.txt
```

## Configuración

Crear archivo `.env` con:

```
GROQ_API_KEY=tu_api_key_aqui
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
| POST | `/api/analysis/ejecutar` | Ejecutar análisis completo |

## Dashboard

Acceder a `http://localhost:8000/static/index.html` para ver el panel de control.

## Estructura del proyecto

```
ejercicio2/
├── app/
│   ├── agents/        # Agentes IA (CrewAI)
│   ├── tools/         # Herramientas de cada agente
│   ├── models/        # Modelos de base de datos
│   ├── routes/        # Endpoints API
│   ├── dashboard/     # Frontend
│   ├── config.py      # Configuración
│   └── main.py        # Servidor FastAPI
├── retailnova_db.sql  # Script SQL de la BD
├── requirements.txt   # Dependencias
└── run.py             # Punto de entrada
```
