from pydantic import BaseModel


class SendCodeRequest(BaseModel):
    phone: str


class ResetPasswordRequest(BaseModel):
    phone: str
    code: str
    new_password: str
