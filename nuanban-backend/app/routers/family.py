from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, date
from app.db.session import get_db
from app.models.user import User
from app.models.family import FamilyRelation, ElderProfile
from app.models.medication import MedicationLog, MedicationPlan
from app.models.health import HealthRecord
from app.schemas.family import (
    FamilyRelationCreate, FamilyRelationResponse,
    ElderProfileCreate, ElderProfileUpdate,
    ElderProfileResponse, ElderWithProfileResponse
)
from app.dependencies import get_current_user

router = APIRouter(prefix="/api/family", tags=["家庭关系"])


# 子女绑定老人
@router.post("/bind", response_model=FamilyRelationResponse)
def bind_elder(
    data: FamilyRelationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "child":
        raise HTTPException(status_code=403, detail="只有子女角色可以绑定老人")

    elder = db.query(User).filter(User.id == data.elder_user_id, User.role == "elder").first()
    if not elder:
        raise HTTPException(status_code=404, detail="老人用户不存在")

    existing = db.query(FamilyRelation).filter(
        FamilyRelation.child_user_id == current_user.id,
        FamilyRelation.elder_user_id == data.elder_user_id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="已经绑定过该老人")

    relation = FamilyRelation(
        child_user_id=current_user.id,
        elder_user_id=data.elder_user_id,
        relation_type=data.relation_type
    )
    db.add(relation)
    db.commit()
    db.refresh(relation)
    return relation


# 子女查看绑定的老人列表
@router.get("/elders", response_model=List[ElderWithProfileResponse])
def get_my_elders(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "child":
        raise HTTPException(status_code=403, detail="只有子女角色可以查看")

    relations = db.query(FamilyRelation).filter(
        FamilyRelation.child_user_id == current_user.id
    ).all()

    result = []
    for rel in relations:
        elder = db.query(User).filter(User.id == rel.elder_user_id).first()
        profile = db.query(ElderProfile).filter(ElderProfile.user_id == rel.elder_user_id).first()
        result.append({
            "id": elder.id,
            "username": elder.username,
            "phone": elder.phone,
            "role": elder.role,
            "profile": profile,
            "relation_type": rel.relation_type
        })
    return result


# 老人查看绑定的子女列表
@router.get("/children")
def get_my_children(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "elder":
        raise HTTPException(status_code=403, detail="只有老人角色可以查看")

    relations = db.query(FamilyRelation).filter(
        FamilyRelation.elder_user_id == current_user.id
    ).all()

    result = []
    for rel in relations:
        child = db.query(User).filter(User.id == rel.child_user_id).first()
        if child:
            result.append({
                "id": child.id,
                "username": child.username,
                "phone": child.phone,
                "role": child.role,
                "relation_type": rel.relation_type
            })
    return result


# 子女解绑老人
@router.delete("/unbind/{elder_user_id}")
def unbind_elder(
    elder_user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "child":
        raise HTTPException(status_code=403, detail="只有子女角色可以解绑")

    relation = db.query(FamilyRelation).filter(
        FamilyRelation.child_user_id == current_user.id,
        FamilyRelation.elder_user_id == elder_user_id
    ).first()

    if not relation:
        raise HTTPException(status_code=404, detail="未找到绑定关系")

    db.delete(relation)
    db.commit()

    return {"message": "解绑成功"}


# 创建/更新老人档案
@router.post("/profile", response_model=ElderProfileResponse)
def create_elder_profile(
    data: ElderProfileCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    existing = db.query(ElderProfile).filter(ElderProfile.user_id == data.user_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="档案已存在，请使用更新接口")

    profile = ElderProfile(**data.model_dump())
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile


@router.put("/profile/{user_id}", response_model=ElderProfileResponse)
def update_elder_profile(
    user_id: int,
    data: ElderProfileUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    profile = db.query(ElderProfile).filter(ElderProfile.user_id == user_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="档案不存在")

    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(profile, key, value)

    db.commit()
    db.refresh(profile)
    return profile


# 获取老人档案
@router.get("/profile/{user_id}", response_model=ElderProfileResponse)
def get_elder_profile(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    profile = db.query(ElderProfile).filter(ElderProfile.user_id == user_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="档案不存在")
    return profile


# 子女通过手机号绑定老人
@router.post("/bind-by-phone", response_model=FamilyRelationResponse)
def bind_elder_by_phone(
    data: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "child":
        raise HTTPException(status_code=403, detail="只有子女角色可以绑定老人")

    phone = data.get("phone")
    if not phone:
        raise HTTPException(status_code=400, detail="请输入手机号")

    elder = db.query(User).filter(User.phone == phone, User.role == "elder").first()
    if not elder:
        raise HTTPException(status_code=404, detail="未找到该手机号对应的老人账号")

    existing = db.query(FamilyRelation).filter(
        FamilyRelation.child_user_id == current_user.id,
        FamilyRelation.elder_user_id == elder.id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="已经绑定过该老人")

    relation = FamilyRelation(
        child_user_id=current_user.id,
        elder_user_id=elder.id,
        relation_type=data.get("relation_type", "子女")
    )
    db.add(relation)
    db.commit()
    db.refresh(relation)
    return relation


# 获取综合提醒（用药+健康）
@router.get("/alerts/{elder_user_id}")
def get_elder_alerts(
    elder_user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    today = date.today()

    medication_logs = db.query(MedicationLog).filter(
        MedicationLog.elder_user_id == elder_user_id,
        MedicationLog.created_at >= datetime.combine(today, datetime.min.time())
    ).order_by(MedicationLog.created_at.desc()).all()

    health_records = db.query(HealthRecord).filter(
        HealthRecord.elder_user_id == elder_user_id,
        HealthRecord.recorded_at >= datetime.combine(today, datetime.min.time())
    ).order_by(HealthRecord.recorded_at.desc()).all()

    alerts = []

    for log in medication_logs:
        plan = db.query(MedicationPlan).filter(MedicationPlan.id == log.plan_id).first()
        if plan:
            alerts.append({
                "type": "medication",
                "icon": "💊",
                "title": f"已服用{plan.medication_name}",
                "content": f"今日已服用{plan.medication_name}",
                "time": log.taken_at.strftime("%H:%M") if log.taken_at else log.created_at.strftime("%H:%M"),
                "created_at": log.created_at
            })

    for record in health_records:
        type_name = {
            "blood_pressure": "血压",
            "heart_rate": "心率",
            "blood_sugar": "血糖",
            "weight": "体重",
            "sleep": "睡眠"
        }.get(record.record_type, record.record_type)

        alerts.append({
            "type": "health",
            "icon": {
                "blood_pressure": "🩺",
                "heart_rate": "❤️",
                "blood_sugar": "🩸",
                "weight": "⚖️",
                "sleep": "😴"
            }.get(record.record_type, "📊"),
            "title": f"记录{type_name}",
            "content": f"{type_name}：{record.value}",
            "time": record.recorded_at.strftime("%H:%M"),
            "created_at": record.recorded_at
        })

    alerts.sort(key=lambda x: x["created_at"], reverse=True)
    return alerts[:10]