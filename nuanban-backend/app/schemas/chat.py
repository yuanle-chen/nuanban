from pydantic import BaseModel
from datetime import datetime
from typing import List


class ChatMessageRequest(BaseModel):
    elder_user_id: int
    message: str


class ChatMessageResponse(BaseModel):
    id: int
    elder_user_id: int
    role: str  # user / assistant / system
    content: str
    created_at: datetime

    class Config:
        from_attributes = True


class ChatHistoryResponse(BaseModel):
    messages: List[ChatMessageResponse]
    total: int