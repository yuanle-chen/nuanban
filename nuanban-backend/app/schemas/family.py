from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class FamilyRelationCreate(BaseModel):
    elder_user_id: int
    relation_type: str = "子女"


class FamilyRelationResponse(BaseModel):
    id: int
    child_user_id: int
    elder_user_id: int
    relation_type: str
    created_at: datetime

    class Config:
        from_attributes = True


class ElderProfileCreate(BaseModel):
    user_id: int
    real_name: str
    age: Optional[int] = None
    gender: Optional[str] = None
    address: Optional[str] = None
    emergency_contact: Optional[str] = None
    emergency_phone: Optional[str] = None


class ElderProfileUpdate(BaseModel):
    real_name: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    address: Optional[str] = None
    emergency_contact: Optional[str] = None
    emergency_phone: Optional[str] = None


class ElderProfileResponse(BaseModel):
    id: int
    user_id: int
    real_name: str
    age: Optional[int] = None
    gender: Optional[str] = None
    address: Optional[str] = None
    emergency_contact: Optional[str] = None
    emergency_phone: Optional[str] = None

    class Config:
        from_attributes = True


class ElderWithProfileResponse(BaseModel):
    id: int
    username: str
    phone: Optional[str] = None
    role: str
    profile: Optional[ElderProfileResponse] = None
    relation_type: Optional[str] = None

    class Config:
        from_attributes = True