from sqlalchemy import Column, Integer, String, TIMESTAMP, Enum, ForeignKey
from sqlalchemy.sql import func
from app.db.base import Base


class EmergencyRecord(Base):
    __tablename__ = "emergency_records"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="记录ID")
    elder_user_id = Column(Integer, ForeignKey("users.id"), nullable=False, comment="老人用户ID")
    alert_type = Column(Enum("sos", "fall", "abnormal", "voice"), nullable=False, comment="报警类型")
    location = Column(String(255), nullable=True, comment="位置描述")
    handled_status = Column(Enum("pending", "contacting", "resolved", "cancelled"), default="pending", comment="处理状态")
    handled_at = Column(TIMESTAMP, nullable=True, comment="处理时间")
    created_at = Column(TIMESTAMP, server_default=func.now(), comment="触发时间")