from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class BatchCreate(BaseModel):
    id: str
    zone_id: str
    stage: str = "LARVAE"
    initial_quantity: float = 0.0
    substrate_type: Optional[str] = None
    notes: Optional[str] = None

class BatchResponse(BaseModel):
    id: str
    zone_id: str
    stage: str
    start_date: datetime
    end_date: Optional[datetime]
    initial_quantity: float
    substrate_type: Optional[str]
    final_yield: Optional[float]
    status: str
    notes: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True

class FeedingCreate(BaseModel):
    batch_id: str
    food_mass_g: float
    food_type: str
    notes: Optional[str] = None

class FeedingResponse(BaseModel):
    id: int
    batch_id: str
    food_mass_g: float
    food_type: str
    notes: Optional[str]
    fed_at: datetime

    class Config:
        from_attributes = True

class MediaFileResponse(BaseModel):
    id: int
    filename: str
    filepath: str
    media_type: str
    zone_id: Optional[str]
    batch_id: Optional[str]
    file_size_bytes: int
    resolution: Optional[str]
    source: str
    captured_at: datetime

    class Config:
        from_attributes = True
