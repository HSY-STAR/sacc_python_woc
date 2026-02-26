# agent.py（完整版）
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain

# 加载环境变量
load_dotenv()

# 初始化DeepSeek LLM
llm = ChatOpenAI(
    model="deepseek-chat",
    openai_api_key=os.getenv("DEEPSEEK_API_KEY"),
    openai_api_base="https://api.deepseek.com/v1",
    temperature=0.7,
    max_tokens=1000
)

# 创建记忆（用于记住对话历史）
memory = ConversationBufferMemory()

# 创建对话链
conversation = ConversationChain(
    llm=llm,
    memory=memory,
    verbose=True  # 显示详细过程
)

print("="*50)
print("🤖 DeepSeek Agent 已启动！")
print("支持功能：")
print("  - 自由对话")
print("  - 记忆上下文")
print("  - 连续对话")
print("输入'退出'结束对话")
print("="*50)

# 对话循环
while True:
    user_input = input("\n你: ")
    
    if user_input.lower() in ['退出', 'exit', 'quit']:
        print("👋 再见！")
        break
    
    try:
        # 获取AI响应
        response = conversation.predict(input=user_input)
        print(f"\nAgent: {response}")
        
    except Exception as e:
        print(f"❌ 错误: {e}")