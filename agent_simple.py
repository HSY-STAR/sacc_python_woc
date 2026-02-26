# agent_simple.py
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain

# 加载环境变量
load_dotenv()

# 初始化DeepSeek
llm = ChatOpenAI(
    model="deepseek-chat",
    openai_api_key=os.getenv("DEEPSEEK_API_KEY"),
    openai_api_base="https://api.deepseek.com/v1",
    temperature=0.7
)

# 创建记忆（记住对话历史）
memory = ConversationBufferMemory()

# 创建对话链（verbose=False 简化输出）
conversation = ConversationChain(
    llm=llm,
    memory=memory,
    verbose=False  # 关键：设为False
)

print("="*50)
print("🤖 AI助手已启动（简化版）")
print("功能：自由对话 + 记忆上下文")
print("输入'退出'结束对话")
print("="*50)

# 对话循环
while True:
    user_input = input("\n你: ")
    
    if user_input.lower() in ['退出', 'exit', 'quit']:
        print("👋 再见！")
        break
    
    try:
        # 获取响应（不再显示中间过程）
        response = conversation.predict(input=user_input)
        print(f"\nAI: {response}")
        print("-"*50)
    except Exception as e:
        print(f"❌ 错误: {e}")