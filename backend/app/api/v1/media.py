from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
import os
import shutil
from datetime import datetime, timezone
from app.database.session import get_db
from app.config import settings
from app.repositories.batch_repo import BatchRepository
from app.schemas.production import MediaFileResponse

router = APIRouter(prefix="/media", tags=["Multimedia y Cámaras"])

@router.get("", response_model=List[MediaFileResponse])
async def list_media(
    zone_id: Optional[str] = None,
    batch_id: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    repo = BatchRepository(db)
    files = await repo.get_media_files(zone_id=zone_id, batch_id=batch_id)
    return [MediaFileResponse.model_validate(f) for f in files]

@router.post("/upload", response_model=MediaFileResponse, status_code=201)
async def upload_real_image(
    file: UploadFile = File(...),
    zone_id: str = Form("ZONE-LAR"),
    batch_id: Optional[str] = Form(None),
    db: AsyncSession = Depends(get_db)
):
    """
    Permite cargar imágenes reales del biorreactor / larvas
    para visualización y entrenamiento fotográfico.
    """
    upload_dir = os.path.join(settings.STORAGE_PATH, "uploads")
    os.makedirs(upload_dir, exist_ok=True)

    timestamp_str = int(datetime.now(timezone.utc).timestamp())
    safe_filename = f"{zone_id}_{timestamp_str}_{file.filename}"
    file_path = os.path.join(upload_dir, safe_filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    file_size = os.path.getsize(file_path)

    repo = BatchRepository(db)
    media = await repo.create_media_file(
        filename=safe_filename,
        filepath=file_path,
        zone_id=zone_id,
        batch_id=batch_id,
        file_size_bytes=file_size,
        resolution="custom",
        source="upload"
    )

    return MediaFileResponse.model_validate(media)

@router.get("/{media_id}/file")
async def get_media_file(media_id: int, db: AsyncSession = Depends(get_db)):
    repo = BatchRepository(db)
    # Buscar el archivo en base de datos
    files = await repo.get_media_files()
    target = next((f for f in files if f.id == media_id), None)
    if not target or not os.path.exists(target.filepath):
        raise HTTPException(status_code=404, detail="Archivo multimedia no encontrado")
    return FileResponse(target.filepath)
