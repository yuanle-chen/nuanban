from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class HealthRecordCreate(BaseModel):
    elder_user_id: int
    record_type: str  # blood_pressure / heart_rate / blood_sugar / weight / sleep
    value: str


class HealthRecordResponse(BaseModel):
    id: int
    elder_user_id: int
    record_type: str
    value: str
    recorded_at: datetime

    class Config:
        from_attributes = True


class HealthSummary(BaseModel):
    latest_blood_pressure: Optional[str] = None
    latest_heart_rate: Optional[str] = None
    latest_blood_sugar: Optional[str] = None
    latest_weight: Optional[str] = None
    latest_sleep: Optional[str] = None
    blood_pressure_status: Optional[str] = None
    heart_rate_status: Optional[str] = None
    blood_sugar_status: Optional[str] = None
    sleep_status: Optional[str] = None
    status: str = "正常"