from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from app.db.session import get_db
from app.models.user import User
from app.models.emergency import EmergencyRecord
from app.models.family import FamilyRelation
from app.schemas.emergency import EmergencyCreate, EmergencyUpdate, EmergencyResponse
from app.dependencies import get_current_user

router = APIRouter(prefix="/api/emergency", tags=["紧急求助"])


# 触发紧急求助（老人端）
@router.post("/sos", response_model=EmergencyResponse)
def trigger_sos(
    data: EmergencyCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    record = EmergencyRecord(**data.model_dump())
    db.add(record)
    db.commit()
    db.refresh(record)

    # TODO: 这里可以加推送通知给子女
    # push_notification(elder_user_id, "紧急求助！")

    return record


# 取消求助
@router.put("/cancel/{record_id}", response_model=EmergencyResponse)
def cancel_emergency(
    record_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    record = db.query(EmergencyRecord).filter(EmergencyRecord.id == record_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="求助记录不存在")

    record.handled_status = "cancelled"
    record.handled_at = datetime.now()
    db.commit()
    db.refresh(record)
    return record


# 获取老人求助历史
@router.get("/history", response_model=List[EmergencyResponse])
def get_emergency_history(
    elder_user_id: int,
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    records = db.query(EmergencyRecord).filter(
        EmergencyRecord.elder_user_id == elder_user_id
    ).order_by(EmergencyRecord.created_at.desc()).limit(limit).all()
    return records


# 子女查看绑定老人的未处理求助
@router.get("/pending", response_model=List[EmergencyResponse])
def get_pending_emergencies(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "child":
        raise HTTPException(status_code=403, detail="只有子女角色可以查看")

    # 找到绑定的老人
    relations = db.query(FamilyRelation).filter(
        FamilyRelation.child_user_id == current_user.id
    ).all()
    elder_ids = [r.elder_user_id for r in relations]

    if not elder_ids:
        return []

    records = db.query(EmergencyRecord).filter(
        EmergencyRecord.elder_user_id.in_(elder_ids),
        EmergencyRecord.handled_status == "pending"
    ).order_by(EmergencyRecord.created_at.desc()).all()
    return records


# 更新处理状态（子女/社区）
@router.put("/handle/{record_id}", response_model=EmergencyResponse)
def handle_emergency(
    record_id: int,
    data: EmergencyUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    record = db.query(EmergencyRecord).filter(EmergencyRecord.id == record_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="求助记录不存在")

    record.handled_status = data.handled_status
    if data.handled_status in ["resolved", "cancelled"]:
        record.handled_at = datetime.now()

    db.commit()
    db.refresh(record)
    return record