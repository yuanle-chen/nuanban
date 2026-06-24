from sqlalchemy import Column, Integer, String, TIMESTAMP, Enum, ForeignKey, Boolean, JSON
from sqlalchemy.sql import func
from app.db.base import Base


class MedicationPlan(Base):
    __tablename__ = "medication_plans"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="计划ID")
    elder_user_id = Column(Integer, ForeignKey("users.id"), nullable=False, comment="老人用户ID")
    medication_name = Column(String(100), nullable=False, comment="药物名称")
    dosage = Column(String(50), nullable=False, comment="剂量")
    frequency = Column(String(50), nullable=False, comment="服用频率")
    reminder_times = Column(JSON, nullable=False, comment="提醒时间列表")
    is_active = Column(Boolean, default=True, comment="是否启用")
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())


class MedicationLog(Base):
    __tablename__ = "medication_logs"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="记录ID")
    plan_id = Column(Integer, ForeignKey("medication_plans.id"), nullable=False, comment="计划ID")
    elder_user_id = Column(Integer, ForeignKey("users.id"), nullable=False, comment="老人用户ID")
    scheduled_time = Column(String(10), nullable=False, comment="计划时间 HH:MM")
    taken_at = Column(TIMESTAMP, nullable=True, comment="实际服用时间")
    status = Column(Enum("pending", "taken", "missed"), default="pending", comment="状态")
    created_at = Column(TIMESTAMP, server_default=func.now())