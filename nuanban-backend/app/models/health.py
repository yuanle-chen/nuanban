from sqlalchemy import Column, Integer, String, TIMESTAMP, Enum, ForeignKey
from sqlalchemy.sql import func
from app.db.base import Base


class HealthRecord(Base):
    __tablename__ = "health_records"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="记录ID")
    elder_user_id = Column(Integer, ForeignKey("users.id"), nullable=False, comment="老人用户ID")
    record_type = Column(Enum("blood_pressure", "heart_rate", "blood_sugar", "weight", "sleep"), nullable=False, comment="记录类型")
    value = Column(String(50), nullable=False, comment="测量值")
    recorded_at = Column(TIMESTAMP, server_default=func.now(), comment="记录时间")