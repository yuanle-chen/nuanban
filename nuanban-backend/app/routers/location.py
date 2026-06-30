from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.session import get_db
from app.models.user import User
from app.models.location import LocationRecord
from app.schemas.location import LocationCreate, LocationResponse
from app.dependencies import get_current_user

router = APIRouter(prefix="/api/location", tags=["位置管理"])


@router.post("/report", response_model=LocationResponse)
def report_location(
    data: LocationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    record = LocationRecord(**data.model_dump())
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


@router.get("/latest/{elder_user_id}", response_model=Optional[LocationResponse])
def get_latest_location(
    elder_user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    latest = db.query(LocationRecord).filter(
        LocationRecord.elder_user_id == elder_user_id
    ).order_by(LocationRecord.created_at.desc()).first()
    return latest


@router.get("/history/{elder_user_id}", response_model=List[LocationResponse])
def get_location_history(
    elder_user_id: int,
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    records = db.query(LocationRecord).filter(
        LocationRecord.elder_user_id == elder_user_id
    ).order_by(LocationRecord.created_at.desc()).limit(limit).all()
    return records
