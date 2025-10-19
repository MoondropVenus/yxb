#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
魔搭ModelScope API集成示例
演示如何使用魔搭API进行大模型推理
"""

import asyncio
import sys
import os

# 添加当前目录到 Python 路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def install_openai_package():
    """安装openai包（如果尚未安装）"""
    try:
        import openai
        print("openai包已安装")
        return True
    except ImportError:
        print("正在安装openai包...")
        import subprocess
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "openai"])
            print("openai包安装成功")
            return True
        except subprocess.CalledProcessError:
            print("openai包安装失败")
            return False

def get_model_answer_with_modelscope(question_text):
    """使用魔搭ModelScope API获取模型答案"""
    # 首先检查是否安装了openai包
    if not install_openai_package():
        return "无法安装openai包，请手动安装：pip install openai"
    
    try:
        from openai import OpenAI
        
        # 配置魔搭ModelScope API
        client = OpenAI(
            base_url='https://api-inference.modelscope.cn/v1',
            api_key='ms-0f3fca09-39fd-4b3b-84b8-74243108fe9e'  # 这里使用您提供的API密钥
        )
        
        # 构造消息
        messages = [
            {
                "role": "system",
                "content": "你是一个智能答题助手，请根据题目选择正确答案并给出解析。"
            },
            {
                "role": "user",
                "content": f"请解答以下选择题:\n{question_text}"
            }
        ]
        
        print("正在调用魔搭ModelScope API...")
        
        # 调用API
        response = client.chat.completions.create(
            model='Qwen/Qwen3-Coder-30B-A3B-Instruct',  # 使用您指定的模型
            messages=messages,
            stream=False  # 不使用流式输出以简化处理
        )
        
        # 提取回答
        answer = response.choices[0].message.content
        return answer
        
    except Exception as e:
        return f"调用API时出错: {str(e)}"

def modelscope_api_demo():
    """魔搭API集成演示"""
    print("魔搭ModelScope API集成演示")
    print("=" * 40)
    
    # 示例选择题
    sample_questions = """
1. 人工智能的英文缩写是什么？
A. AI
B. ML
C. DL
D. NN

2. Python是一种什么类型的编程语言？
A. 编译型
B. 解释型
C. 汇编型
D. 机器语言
"""
    
    print("示例选择题:")
    print(sample_questions)
    
    print("\n正在使用魔搭ModelScope API获取答案...")
    
    # 获取模型回答
    answer = get_model_answer_with_modelscope(sample_questions)
    
    print("\n模型回答:")
    print(answer)
    
    print("\n" + "=" * 40)
    print("魔搭API集成演示完成！")

if __name__ == "__main__":
    modelscope_api_demo()