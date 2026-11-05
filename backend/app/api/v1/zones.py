from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.database.session import get_db
from app.repositories.zones_repo import ZonesRepository
from app.repositories.telemetry_repo import TelemetryRepository
from app.schemas.telemetry import ZoneResponse, SensorResponse, SensorReadingResponse

router = APIRouter(prefix="/zones", tags=["Zonas"])

@router.get("", response_model=List[ZoneResponse])
async def list_zones(db: AsyncSession = Depends(get_db)):
    zones_repo = ZonesRepository(db)
    telemetry_repo = TelemetryRepository(db)

    zones = await zones_repo.get_all_zones()
    latest_readings = await telemetry_repo.get_latest_readings_all()
    latest_map = {r.sensor_id: r for r in latest_readings}

    response_zones = []
    for z in zones:
        sensor_list = []
        for s in z.sensors:
            s_resp = SensorResponse.model_validate(s)
            if s.id in latest_map:
                s_resp.latest_reading = SensorReadingResponse.model_validate(latest_map[s.id])
            sensor_list.append(s_resp)

        z_resp = ZoneResponse(
            id=z.id,
            name=z.name,
            description=z.description,
            status=z.status,
            sensors=sensor_list
        )
        response_zones.append(z_resp)

    return response_zones

@router.get("/{zone_id}", response_model=ZoneResponse)
async def get_zone(zone_id: str, db: AsyncSession = Depends(get_db)):
    zones_repo = ZonesRepository(db)
    telemetry_repo = TelemetryRepository(db)

    zone = await zones_repo.get_zone_by_id(zone_id)
    if not zone:
        raise HTTPException(status_code=404, detail=f"Zona {zone_id} no encontrada")

    latest_readings = await telemetry_repo.get_latest_readings_all()
    latest_map = {r.sensor_id: r for r in latest_readings}

    sensor_list = []
    for s in zone.sensors:
        s_resp = SensorResponse.model_validate(s)
        if s.id in latest_map:
            s_resp.latest_reading = SensorReadingResponse.model_validate(latest_map[s.id])
        sensor_list.append(s_resp)

    return ZoneResponse(
        id=zone.id,
        name=zone.name,
        description=zone.description,
        status=zone.status,
        sensors=sensor_list
    )
