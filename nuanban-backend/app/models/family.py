from sqlalchemy import Column, Integer, String, TIMESTAMP, Enum, ForeignKey
from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base import Base


class FamilyRelation(Base):
    __tablename__ = "family_relations"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="关系ID")
    child_user_id = Column(Integer, ForeignKey("users.id"), nullable=False, comment="子女用户ID")
    elder_user_id = Column(Integer, ForeignKey("users.id"), nullable=False, comment="老人用户ID")
    relation_type = Column(String(20), default="子女", comment="关系类型")
    created_at = Column(TIMESTAMP, server_default=func.now(), comment="创建时间")

    child = relationship("User", foreign_keys=[child_user_id])
    elder = relationship("User", foreign_keys=[elder_user_id])


class ElderProfile(Base):
    __tablename__ = "elder_profiles"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="档案ID")
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True, comment="用户ID")
    real_name = Column(String(50), nullable=False, comment="真实姓名")
    age = Column(Integer, comment="年龄")
    gender = Column(Enum("male", "female"), comment="性别")
    address = Column(String(255), comment="住址")
    emergency_contact = Column(String(100), comment="紧急联系人")
    emergency_phone = Column(String(20), comment="紧急联系电话")
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())