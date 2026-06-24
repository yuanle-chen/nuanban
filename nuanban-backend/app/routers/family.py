from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.models.user import User
from app.models.family import FamilyRelation, ElderProfile
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