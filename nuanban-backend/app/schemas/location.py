from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class LocationCreate(BaseModel):
    elder_user_id: int
    latitude: float
    longitude: float
    address: Optional[str] = None


class LocationResponse(BaseModel):
    id: int
    elder_user_id: int
    latitude: float
    longitude: float
    address: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True
