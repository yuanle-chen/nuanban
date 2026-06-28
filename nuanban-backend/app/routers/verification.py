import random
import string
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.user import User
from app.models.verification_code import VerificationCode
from app.schemas.verification import SendCodeRequest, ResetPasswordRequest
from app.core.security import get_password_hash
from app.dependencies import get_current_user

router = APIRouter(prefix="/api/auth", tags=["认证"])


def generate_code(length: int = 6) -> str:
    """生成6位数字验证码"""
    return ''.join(random.choices(string.digits, k=length))


@router.post("/send-code")
def send_verification_code(
    data: SendCodeRequest,
    db: Session = Depends(get_db)
):
    """发送验证码"""
    # 检查手机号是否已注册
    user = db.query(User).filter(User.phone == data.phone).first()
    if not user:
        raise HTTPException(status_code=404, detail="该手机号未注册")

    # 生成验证码（开发环境直接返回）
    code = generate_code()

    # 删除该手机号之前的未使用验证码
    db.query(VerificationCode).filter(
        VerificationCode.phone == data.phone,
        VerificationCode.is_used == False
    ).delete()

    # 保存新验证码
    expires_at = datetime.now() + timedelta(minutes=10)
    verification = VerificationCode(
        phone=data.phone,
        code=code,
        purpose="reset_password",
        is_used=False,
        expires_at=expires_at
    )
    db.add(verification)
    db.commit()

    # TODO: 真实环境需要接入短信服务发送验证码
    # 这里模拟发送，返回验证码（开发测试用）
    # 生产环境应该删除这行，只发送短信
    print(f"【开发测试】验证码: {code}")

    return {
        "message": "验证码已发送",
        # 开发环境下返回验证码方便测试，生产环境应删除此行
        "code": code if True else None  # True 改为 False 可关闭开发测试模式
    }


@router.post("/reset-password")
def reset_password(
    data: ResetPasswordRequest,
    db: Session = Depends(get_db)
):
    """验证验证码并重置密码"""
    # 查找验证码
    verification = db.query(VerificationCode).filter(
        VerificationCode.phone == data.phone,
        VerificationCode.code == data.code,
        VerificationCode.is_used == False
    ).first()

    if not verification:
        raise HTTPException(status_code=400, detail="验证码错误或已过期")

    # 检查是否过期
    if verification.expires_at < datetime.now():
        raise HTTPException(status_code=400, detail="验证码已过期")

    # 查找用户
    user = db.query(User).filter(User.phone == data.phone).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")

    # 更新密码
    user.password = get_password_hash(data.new_password)
    verification.is_used = True
    db.commit()

    return {"message": "密码重置成功，请使用新密码登录"}
