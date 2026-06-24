from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.models.user import User
from app.models.chat import ChatLog
from app.schemas.chat import ChatMessageRequest, ChatMessageResponse, ChatHistoryResponse
from app.services.ai_service import ai_service
from app.dependencies import get_current_user

router = APIRouter(prefix="/api/chat", tags=["AI对话"])


# 发送消息，获取AI回复
@router.post("/message", response_model=ChatMessageResponse)
async def send_chat_message(
        data: ChatMessageRequest,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    # 保存用户消息
    user_msg = ChatLog(
        elder_user_id=data.elder_user_id,
        role="user",
        content=data.message
    )
    db.add(user_msg)
    db.commit()
    db.refresh(user_msg)

    # 获取历史对话
    history = ai_service.get_recent_messages(db, data.elder_user_id, limit=10)

    # 生成AI回复
    reply_content = await ai_service.generate_reply(
        elder_user_id=data.elder_user_id,
        message=data.message,
        history=history
    )

    # 保存AI回复
    assistant_msg = ChatLog(
        elder_user_id=data.elder_user_id,
        role="assistant",
        content=reply_content
    )
    db.add(assistant_msg)
    db.commit()
    db.refresh(assistant_msg)

    return assistant_msg


# 获取对话历史
@router.get("/history", response_model=ChatHistoryResponse)
def get_chat_history(
        elder_user_id: int,
        limit: int = 50,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    messages = db.query(ChatLog).filter(
        ChatLog.elder_user_id == elder_user_id
    ).order_by(ChatLog.created_at.desc()).limit(limit).all()

    # 倒序返回（最早的在前）
    messages.reverse()

    return {
        "messages": messages,
        "total": len(messages)
    }