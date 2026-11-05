from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from typing import List, Optional, Dict
from datetime import datetime
from app.models.entities import SensorReading, Sensor, Alert
from app.schemas.telemetry import SensorReadingCreate

class TelemetryRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_reading(self, reading_in: SensorReadingCreate) -> SensorReading:
        reading = SensorReading(
            sensor_id=reading_in.sensor_id,
            zone_id=reading_in.zone_id,
            device_id=reading_in.device_id,
            batch_id=reading_in.batch_id,
            variable=reading_in.variable,
            value=reading_in.value,
            unit=reading_in.unit,
            source=reading_in.source,
            quality=reading_in.quality,
            recorded_at=reading_in.recorded_at
        )
        self.session.add(reading)
        await self.session.commit()
        await self.session.refresh(reading)
        return reading

    async def get_latest_readings_all(self) -> List[SensorReading]:
        """Obtiene la última lectura de cada sensor mediante subquery"""
        stmt = (
            select(SensorReading)
            .distinct(SensorReading.sensor_id)
            .order_by(SensorReading.sensor_id, desc(SensorReading.recorded_at))
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_sensor_history(
        self,
        sensor_id: str,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        limit: int = 100
    ) -> List[SensorReading]:
        query = select(SensorReading).where(SensorReading.sensor_id == sensor_id)
        if start_time:
            query = query.where(SensorReading.recorded_at >= start_time)
        if end_time:
            query = query.where(SensorReading.recorded_at <= end_time)
        query = query.order_by(desc(SensorReading.recorded_at)).limit(limit)

        result = await self.session.execute(query)
        readings = list(result.scalars().all())
        # Devolver en orden cronológico ascendente para graficar
        readings.reverse()
        return readings

    async def get_zone_history(
        self,
        zone_id: str,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        limit: int = 300
    ) -> List[SensorReading]:
        query = select(SensorReading).where(SensorReading.zone_id == zone_id)
        if start_time:
            query = query.where(SensorReading.recorded_at >= start_time)
        if end_time:
            query = query.where(SensorReading.recorded_at <= end_time)
        query = query.order_by(desc(SensorReading.recorded_at)).limit(limit)

        result = await self.session.execute(query)
        readings = list(result.scalars().all())
        readings.reverse()
        return readings

    async def get_active_alerts(self) -> List[Alert]:
        query = select(Alert).where(Alert.is_resolved == False).order_by(desc(Alert.created_at))
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def create_alert(self, zone_id: str, title: str, message: str, severity: str = "WARNING", sensor_id: Optional[str] = None) -> Alert:
        alert = Alert(
            zone_id=zone_id,
            sensor_id=sensor_id,
            severity=severity,
            title=title,
            message=message,
            is_resolved=False
        )
        self.session.add(alert)
        await self.session.commit()
        await self.session.refresh(alert)
        return alert
