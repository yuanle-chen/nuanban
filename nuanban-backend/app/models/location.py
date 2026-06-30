from sqlalchemy import Column, BigInteger, String, Float, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from app.db.base import Base


class LocationRecord(Base):
    __tablename__ = "location_records"

    id = Column(BigInteger, primary_key=True, autoincrement=True, comment="记录ID")
    elder_user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False, comment="老人用户ID")
    latitude = Column(Float, nullable=False, comment="纬度")
    longitude = Column(Float, nullable=False, comment="经度")
    address = Column(String(255), nullable=True, comment="地址描述")
    created_at = Column(TIMESTAMP, server_default=func.now(), comment="上报时间")
