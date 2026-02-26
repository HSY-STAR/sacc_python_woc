# agent_with_tools.py
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.agents import initialize_agent, AgentType
from langchain.tools import Tool
from tools import Tools

# 加载环境变量
load_dotenv()

# 初始化LLM
llm = ChatOpenAI(
    model="deepseek-chat",
    openai_api_key=os.getenv("DEEPSEEK_API_KEY"),
    openai_api_base="https://api.deepseek.com/v1",
    temperature=0.7,
    max_tokens=1000
)

# 创建工具实例
tools_instance = Tools()

# 定义工具列表
tools = [
    Tool(
        name="天气查询",
        func=tools_instance.get_weather,
        description="查询城市的实时天气，输入城市名称"
    ),
    Tool(
        name="读取文件",
        func=tools_instance.read_file,
        description="读取指定文件的内容，输入文件路径"
    ),
    Tool(
        name="写入文件",
        func=tools_instance.write_file,
        description="向文件写入内容，输入格式：文件路径|内容"
    ),
    Tool(
        name="当前时间",
        func=tools_instance.get_time,
        description="获取当前日期和时间"
    ),
    Tool(
        name="计算器",
        func=tools_instance.calculator,
        description="进行数学计算，输入数学表达式"
    )
]

# 创建记忆
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# 初始化Agent
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
    memory=memory,
    verbose=True,
    handle_parsing_errors=True
)

print("="*50)
print("🤖 智能Agent已启动（带工具集）")
print("可用工具：天气查询、文件读写、时间查询、计算器")
print("输入'退出'结束对话")
print("="*50)

# 对话循环
while True:
    user_input = input("\n你: ")
    
    if user_input.lower() in ['退出', 'exit', 'quit']:
        print("👋 再见！")
        break
    
    try:
        response = agent.run(user_input)
        print(f"\nAgent: {response}")
    except Exception as e:
        print(f"❌ 错误: {e}")