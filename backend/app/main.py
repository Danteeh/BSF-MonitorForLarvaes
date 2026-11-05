import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.mqtt.client import mqtt_consumer
from app.websocket.manager import ws_manager
from app.api.v1.zones import router as zones_router
from app.api.v1.sensors import router as sensors_router
from app.api.v1.batches import router as batches_router
from app.api.v1.media import router as media_router
from app.api.v1.system import router as system_router
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("bsf.main")

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Initializing BSF MONITOR Backend...")
    # Iniciar consumidor MQTT con el event loop actual
    loop = asyncio.get_running_loop()
    mqtt_consumer.start(loop)
    yield
    logger.info("Shutting down BSF MONITOR Backend...")
    mqtt_consumer.stop()

app = FastAPI(
    title="BSF MONITOR API",
    description="Plataforma de Monitoreo y Analítica para Biorreactor de Mosca Soldado Negra",
    version="1.0.0",
    lifespan=lifespan
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rutas API v1
app.include_router(system_router, prefix="/api/v1")
app.include_router(zones_router, prefix="/api/v1")
app.include_router(sensors_router, prefix="/api/v1")
app.include_router(batches_router, prefix="/api/v1")
app.include_router(media_router, prefix="/api/v1")

@app.websocket("/ws/telemetry")
async def websocket_telemetry_endpoint(websocket: WebSocket):
    await ws_manager.connect(websocket)
    try:
        # Enviar mensaje de bienvenida y estado
        await websocket.send_json({
            "type": "connection_established",
            "message": "Connected to BSF MONITOR Telemetry Stream",
            "mode": settings.BSF_MODE
        })
        while True:
            # Mantener conexión viva y permitir comandos entrantes si el cliente los envía
            data = await websocket.receive_text()
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)
    except Exception as e:
        logger.warning(f"WebSocket error: {e}")
        ws_manager.disconnect(websocket)

@app.get("/")
async def root():
    return {
        "project": "BSF MONITOR",
        "description": "Black Soldier Fly Bioreactor IoT Platform",
        "status": "online",
        "mode": settings.BSF_MODE,
        "docs_url": "/docs"
    }
