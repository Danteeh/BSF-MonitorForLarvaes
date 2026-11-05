from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from typing import List
from datetime import datetime, timezone
from app.database.session import get_db
from app.config import settings
from app.repositories.zones_repo import ZonesRepository
from app.repositories.telemetry_repo import TelemetryRepository
from app.mqtt.client import mqtt_consumer
from app.schemas.telemetry import (
    SystemStatusResponse,
    AlertResponse,
    SimulatorControlRequest,
    FaultInjectionRequest
)
from app.websocket.manager import ws_manager

router = APIRouter(prefix="/system", tags=["Sistema & Diagnóstico"])

@router.get("/status", response_model=SystemStatusResponse)
async def system_status(db: AsyncSession = Depends(get_db)):
    zones_repo = ZonesRepository(db)
    zones = await zones_repo.get_all_zones()
    sensors = await zones_repo.get_all_sensors()

    db_ok = False
    try:
        await db.execute(text("SELECT 1"))
        db_ok = True
    except Exception:
        db_ok = False

    return SystemStatusResponse(
        mode=settings.BSF_MODE,
        status="OPERATIONAL" if db_ok else "DEGRADED",
        backend_version="1.0.0-beta",
        active_zones=len(zones),
        active_sensors=len(sensors),
        mqtt_connected=mqtt_consumer.is_connected,
        database_connected=db_ok,
        timestamp=datetime.now(timezone.utc)
    )

@router.get("/alerts", response_model=List[AlertResponse])
async def list_alerts(db: AsyncSession = Depends(get_db)):
    repo = TelemetryRepository(db)
    alerts = await repo.get_active_alerts()
    return [AlertResponse.model_validate(a) for a in alerts]

@router.post("/simulator/fault")
async def trigger_simulator_fault(req: FaultInjectionRequest):
    """
    Inyecta un fallo simulado que el motor de simulación o HAL captará
    para probar la robustez del monitoreo y visualización.
    """
    payload = {
        "sensor_id": req.sensor_id,
        "fault_type": req.fault_type,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

    # Publicar en broker MQTT para el motor del simulador
    mqtt_consumer.publish("bsf/simulator/command", payload)

    # Transmitir a WebSockets
    await ws_manager.broadcast_json({
        "type": "simulator_fault",
        "data": payload
    })
    return {"message": f"Fallo '{req.fault_type}' inyectado para sensor '{req.sensor_id}'"}
