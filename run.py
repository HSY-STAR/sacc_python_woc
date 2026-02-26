import uvicorn

if __name__ == "__main__":
    # 启动 FastAPI 应用
    uvicorn.run(
        "app.main:app",    # 应用导入路径
        host="127.0.0.1",  # 监听地址（localhost）
        port=8000,         # 监听端口
        reload=True,       # 开发模式：代码修改后自动重启
        log_level="info"   # 日志级别
    )