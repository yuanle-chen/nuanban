from sqlalchemy import Column, BigInteger, String, TIMESTAMP, Text, ForeignKey
from sqlalchemy.sql import func
from app.db.base import Base


class ChatLog(Base):
    __tablename__ = "chat_logs"

    id = Column(BigInteger, primary_key=True, autoincrement=True, comment="记录ID")
    elder_user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False, comment="老人用户ID")
    role = Column(String(20), nullable=False, comment="消息角色")
    content = Column(Text, nullable=False, comment="消息内容")
    created_at = Column(TIMESTAMP, server_default=func.now(), comment="创建时间")