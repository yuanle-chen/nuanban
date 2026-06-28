from sqlalchemy import Column, BigInteger, String, TIMESTAMP, Integer
from sqlalchemy.sql import func
from app.db.base import Base


class VideoCall(Base):
    __tablename__ = "video_calls"

    id = Column(BigInteger, primary_key=True, autoincrement=True, comment="记录ID")
    caller_id = Column(BigInteger, nullable=False, comment="发起人ID")
    receiver_id = Column(BigInteger, nullable=False, comment="接收人ID")
    status = Column(String(20), default="calling", comment="状态：calling=呼叫中, connected=已接通, ended=已结束, missed=未接通")
    duration = Column(Integer, default=0, comment="通话时长（秒）")
    room_id = Column(String(50), comment="房间号")
    started_at = Column(TIMESTAMP, nullable=True, comment="开始时间")
    ended_at = Column(TIMESTAMP, nullable=True, comment="结束时间")
    created_at = Column(TIMESTAMP, server_default=func.now(), comment="创建时间")
