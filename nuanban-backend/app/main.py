from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, family, health, medication, emergency, chat, verification  # ← 加导入

app = FastAPI(
    title="暖伴 · 智能陪伴机器人 API",
    description="老人陪伴 App 的后端服务",
    version="1.0.0"
)

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

@app.get("/")
def root():
    return {"message": "暖伴 API 服务运行中", "version": "1.0.0"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}