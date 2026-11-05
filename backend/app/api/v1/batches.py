from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from app.database.session import get_db
from app.repositories.batch_repo import BatchRepository
from app.schemas.production import (
    BatchCreate,
    BatchResponse,
    FeedingCreate,
    FeedingResponse
)

router = APIRouter(prefix="/batches", tags=["Gestión de Lotes"])

@router.get("", response_model=List[BatchResponse])
async def list_batches(
    status: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db)
):
    repo = BatchRepository(db)
    batches = await repo.get_all_batches(status=status)
    return [BatchResponse.model_validate(b) for b in batches]

@router.post("", response_model=BatchResponse, status_code=201)
async def create_batch(batch_in: BatchCreate, db: AsyncSession = Depends(get_db)):
    repo = BatchRepository(db)
    existing = await repo.get_batch_by_id(batch_in.id)
    if existing:
        raise HTTPException(status_code=400, detail=f"El lote {batch_in.id} ya existe")
    batch = await repo.create_batch(batch_in)
    return BatchResponse.model_validate(batch)

@router.get("/{batch_id}", response_model=BatchResponse)
async def get_batch(batch_id: str, db: AsyncSession = Depends(get_db)):
    repo = BatchRepository(db)
    batch = await repo.get_batch_by_id(batch_id)
    if not batch:
        raise HTTPException(status_code=404, detail=f"Lote {batch_id} no encontrado")
    return BatchResponse.model_validate(batch)

@router.post("/{batch_id}/feedings", response_model=FeedingResponse, status_code=201)
async def add_feeding(
    batch_id: str,
    feeding_in: FeedingCreate,
    db: AsyncSession = Depends(get_db)
):
    repo = BatchRepository(db)
    batch = await repo.get_batch_by_id(batch_id)
    if not batch:
        raise HTTPException(status_code=404, detail=f"Lote {batch_id} no encontrado")
    feeding_in.batch_id = batch_id
    record = await repo.add_feeding(feeding_in)
    return FeedingResponse.model_validate(record)

@router.get("/{batch_id}/feedings", response_model=List[FeedingResponse])
async def list_feedings(batch_id: str, db: AsyncSession = Depends(get_db)):
    repo = BatchRepository(db)
    records = await repo.get_feedings_for_batch(batch_id)
    return [FeedingResponse.model_validate(r) for r in records]
