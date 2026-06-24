from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, date
from app.db.session import get_db
from app.models.user import User
from app.models.medication import MedicationPlan, MedicationLog
from app.schemas.medication import (
    MedicationPlanCreate, MedicationPlanUpdate,
    MedicationPlanResponse, MedicationLogResponse,
    MedicationTodayResponse
)
from app.dependencies import get_current_user

router = APIRouter(prefix="/api/medication", tags=["用药管理"])


# 获取用药计划列表
@router.get("/plans", response_model=List[MedicationPlanResponse])
def get_medication_plans(
        elder_user_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    plans = db.query(MedicationPlan).filter(
        MedicationPlan.elder_user_id == elder_user_id,
        MedicationPlan.is_active == True
    ).all()
    return plans


# 添加用药计划
@router.post("/plans", response_model=MedicationPlanResponse)
def create_medication_plan(
        data: MedicationPlanCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    plan = MedicationPlan(**data.model_dump())
    db.add(plan)
    db.commit()
    db.refresh(plan)
    return plan


# 更新用药计划
@router.put("/plans/{plan_id}", response_model=MedicationPlanResponse)
def update_medication_plan(
        plan_id: int,
        data: MedicationPlanUpdate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    plan = db.query(MedicationPlan).filter(MedicationPlan.id == plan_id).first()
    if not plan:
        raise HTTPException(status_code=404, detail="用药计划不存在")

    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(plan, key, value)

    db.commit()
    db.refresh(plan)
    return plan


# 确认服药
@router.post("/take", response_model=MedicationLogResponse)
def record_medication_taken(
        plan_id: int,
        scheduled_time: str,
        elder_user_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    today = date.today()

    # 查找今日是否已有记录
    log = db.query(MedicationLog).filter(
        MedicationLog.plan_id == plan_id,
        MedicationLog.elder_user_id == elder_user_id,
        MedicationLog.scheduled_time == scheduled_time,
        MedicationLog.created_at >= datetime.combine(today, datetime.min.time())
    ).first()

    if not log:
        log = MedicationLog(
            plan_id=plan_id,
            elder_user_id=elder_user_id,
            scheduled_time=scheduled_time,
            status="taken",
            taken_at=datetime.now()
        )
        db.add(log)
    else:
        log.status = "taken"
        log.taken_at = datetime.now()

    db.commit()
    db.refresh(log)
    return log


# 获取今日用药情况
@router.get("/today", response_model=List[MedicationTodayResponse])
def get_today_medication(
        elder_user_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    today = date.today()
    plans = db.query(MedicationPlan).filter(
        MedicationPlan.elder_user_id == elder_user_id,
        MedicationPlan.is_active == True
    ).all()

    result = []
    for plan in plans:
        times = plan.reminder_times if isinstance(plan.reminder_times, list) else []
        for t in times:
            log = db.query(MedicationLog).filter(
                MedicationLog.plan_id == plan.id,
                MedicationLog.elder_user_id == elder_user_id,
                MedicationLog.scheduled_time == t,
                MedicationLog.created_at >= datetime.combine(today, datetime.min.time())
            ).first()

            result.append({
                "plan_id": plan.id,
                "medication_name": plan.medication_name,
                "dosage": plan.dosage,
                "scheduled_time": t,
                "status": log.status if log else "pending",
                "log_id": log.id if log else None
            })

    # 按时间排序
    result.sort(key=lambda x: x["scheduled_time"])
    return result