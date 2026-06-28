import uuid
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.user import User
from app.models.video_call import VideoCall
from app.schemas.video_call import VideoCallCreate, VideoCallUpdate, VideoCallResponse
from app.dependencies import get_current_user

router = APIRouter(prefix="/api/video-call", tags=["视频通话"])


@router.post("/start", response_model=VideoCallResponse)
def start_video_call(
    data: VideoCallCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """发起视频通话"""
    receiver = db.query(User).filter(User.id == data.receiver_id).first()
    if not receiver:
        raise HTTPException(status_code=404, detail="接收人不存在")

    room_id = str(uuid.uuid4())[:8]

    call = VideoCall(
        caller_id=current_user.id,
        receiver_id=data.receiver_id,
        status="calling",
        room_id=room_id
    )
    db.add(call)
    db.commit()
    db.refresh(call)

    result = VideoCallResponse.model_validate(call)
    result.caller_name = current_user.username
    result.receiver_name = receiver.username
    return result


@router.post("/{call_id}/accept")
def accept_call(
    call_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """接听视频通话"""
    call = db.query(VideoCall).filter(VideoCall.id == call_id).first()
    if not call:
        raise HTTPException(status_code=404, detail="通话记录不存在")

    if call.receiver_id != current_user.id:
        raise HTTPException(status_code=403, detail="无权操作此通话")

    if call.status != "calling":
        raise HTTPException(status_code=400, detail="通话状态异常")

    call.status = "connected"
    call.started_at = datetime.now()
    db.commit()

    return {"message": "已接听", "call_id": call_id, "room_id": call.room_id}


@router.post("/{call_id}/end")
def end_call(
    call_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """结束视频通话"""
    call = db.query(VideoCall).filter(VideoCall.id == call_id).first()
    if not call:
        raise HTTPException(status_code=404, detail="通话记录不存在")

    if call.caller_id != current_user.id and call.receiver_id != current_user.id:
        raise HTTPException(status_code=403, detail="无权操作此通话")

    if call.status in ["ended", "missed"]:
        return {"message": "通话已结束"}

    call.status = "ended"
    call.ended_at = datetime.now()
    if call.started_at:
        call.duration = int((call.ended_at - call.started_at).total_seconds())
    db.commit()

    return {"message": "通话已结束", "duration": call.duration}


@router.get("/pending")
def get_pending_calls(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取待接听的通话"""
    calls = db.query(VideoCall).filter(
        VideoCall.receiver_id == current_user.id,
        VideoCall.status == "calling"
    ).order_by(VideoCall.created_at.desc()).all()

    result = []
    for call in calls:
        caller = db.query(User).filter(User.id == call.caller_id).first()
        item = VideoCallResponse.model_validate(call)
        item.caller_name = caller.username if caller else "未知"
        result.append(item)

    return result


@router.get("/history")
def get_call_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取通话历史记录"""
    calls = db.query(VideoCall).filter(
        (VideoCall.caller_id == current_user.id) | (VideoCall.receiver_id == current_user.id)
    ).order_by(VideoCall.created_at.desc()).limit(20).all()

    result = []
    for call in calls:
        caller = db.query(User).filter(User.id == call.caller_id).first()
        receiver = db.query(User).filter(User.id == call.receiver_id).first()
        item = VideoCallResponse.model_validate(call)
        item.caller_name = caller.username if caller else "未知"
        item.receiver_name = receiver.username if receiver else "未知"
        result.append(item)

    return result
