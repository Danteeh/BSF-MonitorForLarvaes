from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from typing import List, Optional
from app.models.entities import Batch, FeedingRecord, MediaFile
from app.schemas.production import BatchCreate, FeedingCreate

class BatchRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all_batches(self, status: Optional[str] = None) -> List[Batch]:
        query = select(Batch)
        if status:
            query = query.where(Batch.status == status)
        query = query.order_by(desc(Batch.start_date))
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def get_batch_by_id(self, batch_id: str) -> Optional[Batch]:
        query = select(Batch).where(Batch.id == batch_id)
        result = await self.session.execute(query)
        return result.scalars().first()

    async def create_batch(self, batch_in: BatchCreate) -> Batch:
        batch = Batch(
            id=batch_in.id,
            zone_id=batch_in.zone_id,
            stage=batch_in.stage,
            initial_quantity=batch_in.initial_quantity,
            substrate_type=batch_in.substrate_type,
            notes=batch_in.notes
        )
        self.session.add(batch)
        await self.session.commit()
        await self.session.refresh(batch)
        return batch

    async def add_feeding(self, feeding_in: FeedingCreate) -> FeedingRecord:
        record = FeedingRecord(
            batch_id=feeding_in.batch_id,
            food_mass_g=feeding_in.food_mass_g,
            food_type=feeding_in.food_type,
            notes=feeding_in.notes
        )
        self.session.add(record)
        await self.session.commit()
        await self.session.refresh(record)
        return record

    async def get_feedings_for_batch(self, batch_id: str) -> List[FeedingRecord]:
        query = select(FeedingRecord).where(FeedingRecord.batch_id == batch_id).order_by(desc(FeedingRecord.fed_at))
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def get_media_files(self, zone_id: Optional[str] = None, batch_id: Optional[str] = None) -> List[MediaFile]:
        query = select(MediaFile)
        if zone_id:
            query = query.where(MediaFile.zone_id == zone_id)
        if batch_id:
            query = query.where(MediaFile.batch_id == batch_id)
        query = query.order_by(desc(MediaFile.captured_at))
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def create_media_file(
        self,
        filename: str,
        filepath: str,
        zone_id: Optional[str],
        batch_id: Optional[str],
        file_size_bytes: int,
        resolution: Optional[str],
        source: str = "upload"
    ) -> MediaFile:
        media = MediaFile(
            filename=filename,
            filepath=filepath,
            media_type="IMAGE",
            zone_id=zone_id,
            batch_id=batch_id,
            file_size_bytes=file_size_bytes,
            resolution=resolution,
            source=source
        )
        self.session.add(media)
        await self.session.commit()
        await self.session.refresh(media)
        return media
