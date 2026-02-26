# 430 管理系统
基于 FastAPI 的用户管理系统，包含完整的增删改查功能和接口限流。

    必做任务

用户注册（创建）
用户列表（查询）
用户详情（查询）
用户信息更新
用户删除
用户搜索
SQLite数据持久化

    选做任务

Pydantic数据验证（选做1）
接口限流保护（选做2）

    限流策略

| 接口        | 方法    | 限流策略  |
| /users/     | GET    | 30次/分钟 |
| /users/     | POST   | 10次/分钟 |
| /users/{id} | GET    | 30次/分钟 |
| /users/{id} | PUT    | 10次/分钟 |
| /users/{id} | DELETE | 5次/分钟  |
| /users/search/ | GET | 20次/分钟 |

    环境要求

- Python 3.8+
- pip

    安装步骤

1. 克隆项目
git clone [仓库地址]

2. 进入目录
cd fastapi-430-system

3. 创建虚拟环境
python -m venv venv

4. 激活虚拟环境
 Windows:
venv\Scripts\activate
 Linux/Mac:
source venv/bin/activate

5. 安装依赖
pip install -r requirements.txt

6. 运行项目
python run.py

    API文档

启动项目后访问：
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

    项目结构

fastapi-430-system/
├── app/
│   ├── __init__.py
│   ├── main.py              # 主应用入口
│   ├── database/
│   │   ├── __init__.py
│   │   └── database.py      # 数据库配置
│   ├── models/
│   │   ├── __init__.py
│   │   └── user.py          # 数据模型
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── user.py          # 数据验证
│   ├── routers/
│   │   ├── __init__.py
│   │   └── users.py         # API路由
│   └── middleware/
│       ├── __init__.py
│       └── rate_limit.py    # 限流中间件
├── run.py                    # 启动脚本
├── requirements.txt          # 依赖列表
└── README.md                 # 项目说明

    接口测试示例

1.创建用户

curl -X POST "http://127.0.0.1:8000/users/" \
  -H "Content-Type: application/json" \
  -d '{"username":"test","email":"test@test.com","password":"123456"}'
2.获取用户列表

curl "http://127.0.0.1:8000/users/"
    
    注意事项

数据库文件 430_system.db 会自动创建
限流基于IP地址，同一IP超过限制会返回429错误
开发模式支持热重载，修改代码自动重启

    作者 黄诗莹
    
    许可证 MIT