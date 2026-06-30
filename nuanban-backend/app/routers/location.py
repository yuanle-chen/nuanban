from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.session import get_db
from app.models.user import User
from app.models.location import LocationRecord
from app.schemas.location import LocationCreate, LocationResponse
from app.dependencies import get_current_user
from app.utils.amap import regeo_code

router = APIRouter(prefix="/api/location", tags=["位置管理"])

_location_cache = {}


@router.post("/report", response_model=LocationResponse)
async def report_location(
    data: LocationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    cache_key = f"{data.elder_user_id}_{round(data.latitude, 4)}_{round(data.longitude, 4)}"
    address = _location_cache.get(cache_key)
    
    if not address:
        address = await regeo_code(data.latitude, data.longitude)
        if address:
            _location_cache[cache_key] = address
    
    record = LocationRecord(**data.model_dump(exclude={"address"}), address=address or data.address)
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
