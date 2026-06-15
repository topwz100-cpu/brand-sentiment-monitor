"""
FastAPI 主入口
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager

from .config import settings
from .database import init_db
from .routers import brands, news, dashboard
from .services.scheduler import scheduler_service


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    应用生命周期管理
    """
    # 启动时执行
    print("正在初始化数据库...")
    init_db()
    print("数据库初始化完成")
    
    # 启动定时任务
    print("正在启动定时任务...")
    scheduler_service.start()
    
    yield
    
    # 关闭时执行
    print("正在关闭定时任务...")
    scheduler_service.stop()


# 创建FastAPI应用
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="大客户舆情监测系统API",
    lifespan=lifespan
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(brands.router)
app.include_router(news.router)
app.include_router(dashboard.router)


@app.get("/")
def root():
    """根路径"""
    return JSONResponse(
        content={
            "message": "大客户舆情监测系统",
            "version": settings.APP_VERSION,
            "docs": "/docs"
        },
        headers={"Content-Type": "application/json; charset=utf-8"}
    )


@app.get("/health")
def health_check():
    """健康检查"""
    return JSONResponse(
        content={"status": "healthy", "service": "大客户舆情监测系统"},
        headers={"Content-Type": "application/json; charset=utf-8"}
    )
