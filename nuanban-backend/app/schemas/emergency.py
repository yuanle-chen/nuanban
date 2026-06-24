from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class EmergencyCreate(BaseModel):
    elder_user_id: int
    alert_type: str  # sos / fall / abnormal / voice
    location: Optional[str] = None


class EmergencyUpdate(BaseModel):
    handled_status: str  # pending / contacting / resolved / cancelled


class EmergencyResponse(BaseModel):
    id: int
    elder_user_id: int
    alert_type: str
    location: Optional[str] = None
    handled_status: str
    handled_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True