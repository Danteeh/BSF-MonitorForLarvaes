from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from datetime import datetime
from app.database.session import get_db
from app.repositories.zones_repo import ZonesRepository
from app.repositories.telemetry_repo import TelemetryRepository
from app.schemas.telemetry import (
    SensorResponse,
    SensorReadingResponse,
    SensorReadingCreate
)
from app.websocket.manager import ws_manager

router = APIRouter(prefix="/sensors", tags=["Sensores & Telemetría"])

@router.get("", response_model=List[SensorResponse])
async def list_sensors(db: AsyncSession = Depends(get_db)):
    repo = ZonesRepository(db)
    sensors = await repo.get_all_sensors()
    return [SensorResponse.model_validate(s) for s in sensors]

@router.get("/latest", response_model=List[SensorReadingResponse])
async def get_latest_readings(db: AsyncSession = Depends(get_db)):
    repo = TelemetryRepository(db)
    readings = await repo.get_latest_readings_all()
    return [SensorReadingResponse.model_validate(r) for r in readings]

@router.get("/{sensor_id}", response_model=SensorResponse)
async def get_sensor(sensor_id: str, db: AsyncSession = Depends(get_db)):
    repo = ZonesRepository(db)
    sensor = await repo.get_sensor_by_id(sensor_id)
    if not sensor:
        raise HTTPException(status_code=404, detail=f"Sensor {sensor_id} no encontrado")
    return SensorResponse.model_validate(sensor)

@router.get("/{sensor_id}/readings", response_model=List[SensorReadingResponse])
async def get_sensor_readings(
    sensor_id: str,
    start_time: Optional[datetime] = Query(None),
    end_time: Optional[datetime] = Query(None),
    limit: int = Query(100, ge=1, le=1000),
    db: AsyncSession = Depends(get_db)
):
    repo = TelemetryRepository(db)
    readings = await repo.get_sensor_history(sensor_id, start_time, end_time, limit)
    return [SensorReadingResponse.model_validate(r) for r in readings]

@router.post("/readings", response_model=SensorReadingResponse, status_code=201)
async def ingest_reading(reading_in: SensorReadingCreate, db: AsyncSession = Depends(get_db)):
    repo = TelemetryRepository(db)
    reading = await repo.create_reading(reading_in)

    # Broadcast a WebSockets
    await ws_manager.broadcast_json({
        "type": "telemetry",
        "data": {
            "sensor_id": reading.sensor_id,
            "zone_id": reading.zone_id,
            "variable": reading.variable,
            "value": reading.value,
            "unit": reading.unit,
            "source": reading.source,
            "quality": reading.quality,
            "timestamp": reading.recorded_at.isoformat()
        }
    })

    return SensorReadingResponse.model_validate(reading)
