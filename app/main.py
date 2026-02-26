
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.database.database import engine, Base
from app.routers import users

# 导入限流相关
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from app.middleware.rate_limit import limiter, rate_limit_error_handler, RateLimitConfig

# 创建数据库表
Base.metadata.create_all(bind=engine)

# 创建 FastAPI 应用
app = FastAPI(
    title="430 管理系统 API",
    description="用户管理系统（已添加限流保护）",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# 添加限流中间件
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, rate_limit_error_handler)

# 添加 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 包含用户路由
app.include_router(users.router)

# ========== 应用级路由（添加限流）=========

@app.get("/")
@limiter.limit(RateLimitConfig.DEFAULT_LIMITS["loose"])
async def read_root(request: Request):
    """欢迎页面（宽松限流）"""
    return {
        "message": "欢迎使用 430 管理系统 API",
        "version": "1.0.0",
        "rate_limit": "每分钟60次",
        "documentation": {
            "swagger": "/docs",
            "redoc": "/redoc"
        }
    }


@app.get("/health")
@limiter.limit(RateLimitConfig.ENDPOINT_LIMITS["/health"]["GET"])
async def health_check(request: Request):
    """健康检查（宽松限流）"""
    return {
        "status": "healthy",
        "service": "430-management-system",
        "rate_limit_remaining": "每分钟100次"
    }


@app.get("/info")
@limiter.limit(RateLimitConfig.DEFAULT_LIMITS["medium"])
async def system_info(request: Request):
    """系统信息（中等限流）"""
    return {
        "name": "430 管理系统",
        "version": "1.0.0",
        "technologies": ["FastAPI", "SQLAlchemy", "SQLite", "Pydantic"],
        "rate_limits": RateLimitConfig.ENDPOINT_LIMITS
    }