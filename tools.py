# tools.py
import requests
import os
import json
from datetime import datetime
from typing import Optional

class Tools:
    """工具集类"""
    
    @staticmethod
    def get_weather(city: str) -> str:
        """
        获取城市实时天气
        使用 wttr.in 免费天气API
        """
        try:
            # wttr.in 是一个免费天气API
            url = f"https://wttr.in/{city}?format=%C+%t+%w+%h"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                weather_info = response.text.strip()
                return f"{city}的天气：{weather_info}"
            else:
                return f"无法获取{city}的天气信息"
        except Exception as e:
            return f"天气查询失败: {str(e)}"
    
    @staticmethod
    def read_file(file_path: str) -> str:
        """
        读取文件内容
        """
        try:
            if not os.path.exists(file_path):
                return f"文件不存在: {file_path}"
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            return f"文件内容：\n{content[:500]}" + ("..." if len(content) > 500 else "")
        except Exception as e:
            return f"读取文件失败: {str(e)}"
    
    @staticmethod
    def write_file(file_path: str, content: str) -> str:
        """
        写入文件
        """
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return f"成功写入文件: {file_path}"
        except Exception as e:
            return f"写入文件失败: {str(e)}"
    
    @staticmethod
    def get_time() -> str:
        """
        获取当前时间
        """
        now = datetime.now()
        return f"当前时间：{now.strftime('%Y-%m-%d %H:%M:%S')}"
    
    @staticmethod
    def calculator(expression: str) -> str:
        """
        简单计算器
        注意：仅用于安全计算，实际生产环境需要更严格的验证
        """
        try:
            # 只允许数字和基本运算符
            allowed_chars = set("0123456789+-*/(). ")
            if not all(c in allowed_chars for c in expression):
                return "表达式包含非法字符"
            
            result = eval(expression)
            return f"{expression} = {result}"
        except Exception as e:
            return f"计算失败: {str(e)}"

# 测试工具
if __name__ == "__main__":
    tools = Tools()
    print("=== 测试工具集 ===")
    print(tools.get_weather("北京"))
    print(tools.get_time())
    print(tools.calculator("2+3*4"))