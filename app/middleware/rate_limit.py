# app/middleware/rate_limit.py
"""
限流中间件配置
功能: 限制API接口的访问频率，防止恶意刷取
"""

from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
import time

# 创建限流器实例
# key_func=get_remote_address: 基于客户端IP地址进行限流
limiter = Limiter(key_func=get_remote_address)

# 自定义限流错误处理函数
async def rate_limit_error_handler(request: Request, exc: RateLimitExceeded):
    """
    当请求超过限流限制时的错误处理
    """
    return JSONResponse(
        status_code=429,
        content={
            "error": "请求过于频繁",
            "message": "您访问太快了，请稍后再试",
            "retry_after": exc.detail  # 建议等待时间
        }
    )

# 限流策略配置
class RateLimitConfig:
    """限流策略配置类"""
    
    # 全局默认限流
    DEFAULT_LIMITS = {
        "default": "100/minute",      # 默认：每分钟100次
        "strict": "10/minute",        # 严格限制：每分钟10次
        "medium": "30/minute",        # 中等限制：每分钟30次
        "loose": "60/minute"           # 宽松限制：每分钟60次
    }
    
    # 针对不同接口的限流策略
    ENDPOINT_LIMITS = {
        "/users/": {
            "GET": "30/minute",        # 获取列表：每分钟30次
            "POST": "10/minute"         # 创建用户：每分钟10次
        },
        "/users/{user_id}": {
            "GET": "30/minute",        # 获取单个：每分钟30次
            "PUT": "10/minute",         # 更新用户：每分钟10次
            "DELETE": "5/minute"         # 删除用户：每分钟5次（更严格）
        },
        "/users/search/": {
            "GET": "20/minute"          # 搜索：每分钟20次
        },
        "/health": {
            "GET": "100/minute"         # 健康检查：更宽松
        }
    }