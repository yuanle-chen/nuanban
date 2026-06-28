from sqlalchemy import Column, BigInteger, String, TIMESTAMP, Boolean
from sqlalchemy.sql import func
from app.db.base import Base


class VerificationCode(Base):
    __tablename__ = "verification_codes"

    id = Column(BigInteger, primary_key=True, autoincrement=True, comment="记录ID")
    phone = Column(String(20), nullable=False, comment="手机号")
    code = Column(String(10), nullable=False, comment="验证码")
    purpose = Column(String(20), default="reset_password", comment="用途：reset_password=重置密码")
    is_used = Column(Boolean, default=False, comment="是否已使用")
    expires_at = Column(TIMESTAMP, nullable=False, comment="过期时间")
    created_at = Column(TIMESTAMP, server_default=func.now(), comment="创建时间")
