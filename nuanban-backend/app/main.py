from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.routers import auth, family, health, medication, emergency, chat, verification, video_call, location
from app.middleware.exception_handler import (
    http_exception_handler,
    validation_exception_handler,
    general_exception_handler
)

app = FastAPI(
    title="暖伴 · 智能陪伴机器人 API",
    description="老人陪伴 App 的后端服务",
    version="1.0.0"
)

app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册所有路由
app.include_router(auth.router)
app.include_router(family.router)
app.include_router(health.router)
app.include_router(medication.router)
app.include_router(emergency.router)
app.include_router(chat.router)
app.include_router(verification.router)
app.include_router(video_call.router)
app.include_router(location.router)

@app.get("/")
def root():
    return {"message": "暖伴 API 服务运行中", "version": "1.0.0"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}