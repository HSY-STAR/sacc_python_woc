    LangChain Agent 实现
基于 LangChain 和 DeepSeek 的智能Agent系统，支持对话记忆和多种工具调用。


    必做任务
✅ 通过 LangChain 调用API
✅ 完整的工具集（5个工具）

    工具集
1. 天气查询 - 获取城市实时天气
2. 文件读取 - 读取指定文件内容
3. 文件写入 - 创建或写入文件
4. 时间查询 - 获取当前日期时间
5. 计算器 - 数学表达式计算

    环境要求
- Python 3.8+
- pip

    安装步骤
1. 克隆项目
git clone [https://github.com/akwair/sacc_python_woc]
cd langchain-agent
2. 创建虚拟环境
python -m venv venv
3. 激活虚拟环境
#Windows:
venv\Scripts\activate
#Linux/Mac:
source venv/bin/activate
4. 安装依赖
pip install -r requirements.txt
5. 配置环境变量
创建 .env 文件，添加：
DEEPSEEK_API_KEY=your_api_key_here

   使用方法
1. 基础对话Agent
python agent.py
2. 带工具的Agent
python agent_with_tools.py

   工具使用示例
你: 北京天气怎么样？
Agent: 北京的天气：Sunny +15°C
你: 计算 25*4+10
Agent: 25*4+10 = 110
你: 现在几点了？
Agent: 当前时间：2024-02-25 14:30:45
你: 帮我创建test.txt文件，内容是Hello World
Agent: 成功写入文件: test.txt
    
    项目结构
text
langchain-agent/
├── agent.py                 # 基础对话Agent
├── agent_simple.py          # 简化版Agent
├── tools.py                 # 工具集实现
├── agent_with_tools.py      # 带工具的Agent
├── requirements.txt         # 依赖列表
├── README.md                # 项目说明
└── .gitignore               # Git忽略文件
 
     注意事项
API密钥通过 .env 文件配置，不要提交到Git
首次使用需要获取 DeepSeek API Key
工具函数已做错误处理，调用失败会返回友好提示

     作者 黄诗莹

     许可证 MIT