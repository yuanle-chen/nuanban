from pydantic import BaseModel
from typing import Optional


class UserBase(BaseModel):
    username: str
    role: str  # "elder" 或 "child"


class UserCreate(UserBase):
    password: str
    phone: Optional[str] = None


class UserLogin(BaseModel):
    username: str
    password: str


class UserResponse(UserBase):
    id: int
    phone: Optional[str] = None
    avatar: Optional[str] = None

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str


class TokenData(BaseModel):
    username: Optional[str] = None
    user_id: Optional[int] = None


class PasswordChange(BaseModel):
    old_password: str
    new_password: str