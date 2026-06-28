from pydantic import BaseModel
from typing import Optional


class VideoCallCreate(BaseModel):
    receiver_id: int


class VideoCallUpdate(BaseModel):
    status: Optional[str] = None
    duration: Optional[int] = None


class VideoCallResponse(BaseModel):
    id: int
    caller_id: int
    receiver_id: int
    status: str
    duration: int = 0
    room_id: Optional[str] = None
    caller_name: Optional[str] = None
    receiver_name: Optional[str] = None

    class Config:
        from_attributes = True
