from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from typing import List, Optional
from app.models.entities import Zone, Sensor, Device

class ZonesRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all_zones(self) -> List[Zone]:
        query = select(Zone).options(selectinload(Zone.sensors))
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def get_zone_by_id(self, zone_id: str) -> Optional[Zone]:
        query = select(Zone).where(Zone.id == zone_id).options(selectinload(Zone.sensors), selectinload(Zone.devices))
        result = await self.session.execute(query)
        return result.scalars().first()

    async def get_all_sensors(self) -> List[Sensor]:
        query = select(Sensor)
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def get_sensor_by_id(self, sensor_id: str) -> Optional[Sensor]:
        query = select(Sensor).where(Sensor.id == sensor_id)
        result = await self.session.execute(query)
        return result.scalars().first()

    async def get_all_devices(self) -> List[Device]:
        query = select(Device)
        result = await self.session.execute(query)
        return list(result.scalars().all())
