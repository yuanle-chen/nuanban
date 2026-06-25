from sqlalchemy import Column, BigInteger, String, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from app.db.base import Base


class HealthRecord(Base):
    __tablename__ = "health_records"

    id = Column(BigInteger, primary_key=True, autoincrement=True, comment="记录ID")
    elder_user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False, comment="老人用户ID")
    record_type = Column(String(30), nullable=False, comment="记录类型")
    value = Column(String(50), nullable=False, comment="测量值")
    recorded_at = Column(TIMESTAMP, server_default=func.now(), comment="记录时间")