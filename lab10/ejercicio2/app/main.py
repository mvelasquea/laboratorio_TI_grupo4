from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from app.routes import inventory, logistics, forecast, executive, analysis, agents
import os

app = FastAPI(
    title="RetailNova Group - Agentes IA",
    description="Sistema de agentes IA colaborativos para optimización de cadena de suministro",
    version="1.0.0",
)

static_dir = os.path.join(os.path.dirname(__file__), "dashboard", "static")
templates_dir = os.path.join(os.path.dirname(__file__), "dashboard", "templates")

app.mount("/static", StaticFiles(directory=static_dir), name="static")
templates = Jinja2Templates(directory=templates_dir)

app.include_router(inventory.router, prefix="/api/inventory", tags=["Inventarios"])
app.include_router(logistics.router, prefix="/api/logistics", tags=["Logística"])
app.include_router(forecast.router, prefix="/api/forecast", tags=["Pronósticos"])
app.include_router(executive.router, prefix="/api/executive", tags=["Ejecutivo"])
app.include_router(analysis.router, prefix="/api/analysis", tags=["Análisis"])
app.include_router(agents.router, prefix="/api/agents", tags=["Agentes IA"])


@app.get("/", response_class=HTMLResponse)
def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/health")
def health():
    return {"status": "ok"}
