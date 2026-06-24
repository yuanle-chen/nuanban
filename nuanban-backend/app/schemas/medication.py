from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class MedicationPlanCreate(BaseModel):
    elder_user_id: int
    medication_name: str
    dosage: str
    frequency: str
    reminder_times: List[str]  # ["08:00", "12:00", "21:00"]


class MedicationPlanUpdate(BaseModel):
    medication_name: Optional[str] = None
    dosage: Optional[str] = None
    frequency: Optional[str] = None
    reminder_times: Optional[List[str]] = None
    is_active: Optional[bool] = None


class MedicationPlanResponse(BaseModel):
    id: int
    elder_user_id: int
    medication_name: str
    dosage: str
    frequency: str
    reminder_times: List[str]
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class MedicationLogCreate(BaseModel):
    plan_id: int
    elder_user_id: int
    scheduled_time: str


class MedicationLogResponse(BaseModel):
    id: int
    plan_id: int
    elder_user_id: int
    scheduled_time: str
    taken_at: Optional[datetime] = None
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class MedicationTodayResponse(BaseModel):
    plan_id: int
    medication_name: str
    dosage: str
    scheduled_time: str
    status: str
    log_id: Optional[int] = None