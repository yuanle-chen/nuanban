from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.session import get_db
from app.models.user import User
from app.models.health import HealthRecord
from app.schemas.health import HealthRecordCreate, HealthRecordResponse, HealthSummary
from app.dependencies import get_current_user

router = APIRouter(prefix="/api/health", tags=["健康管理"])


# 添加健康记录
@router.post("/records", response_model=HealthRecordResponse)
def add_health_record(
    data: HealthRecordCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    record = HealthRecord(**data.model_dump())
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


# 获取健康记录列表
@router.get("/records", response_model=List[HealthRecordResponse])
def get_health_records(
    elder_user_id: int,
    record_type: Optional[str] = None,
    limit: int = 30,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(HealthRecord).filter(HealthRecord.elder_user_id == elder_user_id)
    if record_type:
        query = query.filter(HealthRecord.record_type == record_type)
    records = query.order_by(HealthRecord.recorded_at.desc()).limit(limit).all()
    return records


# 获取健康数据汇总（最新数据）
@router.get("/summary/{elder_user_id}", response_model=HealthSummary)
def get_health_summary(
    elder_user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    types = ["blood_pressure", "heart_rate", "blood_sugar", "weight", "sleep"]
    summary = HealthSummary()

    for t in types:
        latest = db.query(HealthRecord).filter(
            HealthRecord.elder_user_id == elder_user_id,
            HealthRecord.record_type == t
        ).order_by(HealthRecord.recorded_at.desc()).first()

        if latest:
            if t == "blood_pressure":
                summary.latest_blood_pressure = latest.value
            elif t == "heart_rate":
                summary.latest_heart_rate = latest.value
            elif t == "blood_sugar":
                summary.latest_blood_sugar = latest.value
            elif t == "weight":
                summary.latest_weight = latest.value
            elif t == "sleep":
                summary.latest_sleep = latest.value

    return summary