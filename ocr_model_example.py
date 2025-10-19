#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
OCR文字识别与大模型答题示例
演示如何使用 DrissionPageMCP 截图、OCR识别文字，并使用大模型解答选择题
"""

import asyncio
import sys
import os
import base64

# 添加当前目录到 Python 路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main import DrissionPageMCP

def create_sample_question_image():
    """创建一个包含选择题的示例图片（实际应用中这一步不需要）"""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>示例选择题</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            .question { font-size: 18px; margin-bottom: 15px; }
            .options { margin-left: 20px; }
            .option { margin-bottom: 10px; }
        </style>
    </head>
    <body>
        <h2>示例选择题</h2>
        <div class="question">
            1. 人工智能的英文缩写是什么？
        </div>
        <div class="options">
            <div class="option">A. AI</div>
            <div class="option">B. ML</div>
            <div class="option">C. DL</div>
            <div class="option">D. NN</div>
        </div>
        
        <div class="question">
            2. Python是一种什么类型的编程语言？
        </div>
        <div class="options">
            <div class="option">A. 编译型</div>
            <div class="option">B. 解释型</div>
            <div class="option">C. 汇编型</div>
            <div class="option">D. 机器语言</div>
        </div>
    </body>
    </html>
    """
    
    with open("sample_question.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    
    return os.path.abspath("sample_question.html")

async def ocr_and_model_demo():
    """OCR文字识别与大模型答题演示"""
    print("OCR文字识别与大模型答题演示")
    print("=" * 40)
    
    # 创建 MCP 实例
    mcp = DrissionPageMCP()
    
    # 1. 连接或打开浏览器
    print("1. 正在连接或打开浏览器...")
    try:
        browser_info = await mcp.connect_or_open_browser({
            "debug_port": 9222,
            "headless": False  # 非无头模式，方便观察
        })
        print(f"   浏览器连接成功: {browser_info['browser_address']}")
    except Exception as e:
        print(f"   浏览器连接失败: {e}")
        return
    
    # 2. 创建示例问题页面
    print("\n2. 正在创建示例问题页面...")
    sample_html_path = create_sample_question_image()
    file_url = f"file:///{sample_html_path.replace('\\', '/')}"
    
    try:
        result = await mcp.new_tab(file_url)
        print(f"   示例页面打开成功: {result['title']}")
    except Exception as e:
        print(f"   示例页面打开失败: {e}")
        return
    
    # 3. 等待页面加载
    print("\n3. 等待页面加载...")
    mcp.wait(2)
    
    # 4. 截图并保存
    print("\n4. 正在截图并保存...")
    try:
        screenshot_path = mcp.get_current_tab_screenshot_as_file(".", "sample_questions.png")
        print(f"   截图保存成功: {screenshot_path}")
    except Exception as e:
        print(f"   截图保存失败: {e}")
        return
    
    # 5. 获取页面文本内容（模拟OCR）
    print("\n5. 正在提取页面文本内容（模拟OCR）...")
    try:
        body_text = mcp.get_body_text()
        extracted_text = str(body_text['body_text'])
        print("   提取的文本内容:")
        print("   " + "\n   ".join(extracted_text.split('\n')[:15]))  # 显示前15行
        print("   ...")
    except Exception as e:
        print(f"   文本提取失败: {e}")
        return
    
    # 6. 使用大模型解答问题（模拟）
    print("\n6. 正在使用大模型解答问题...")
    print("   模拟使用魔搭API进行推理:")
    print("   from openai import OpenAI")
    print("   client = OpenAI(")
    print("       base_url='https://api-inference.modelscope.cn/v1',")
    print("       api_key='ms-0f3fca09-39fd-4b3b-84b8-74243108fe9e'")
    print("   )")
    print("   response = client.chat.completions.create(")
    print("       model='Qwen/Qwen3-Coder-30B-A3B-Instruct',")
    print("       messages=[")
    print("           {'role': 'system', 'content': '你是一个智能答题助手，请根据题目选择正确答案。'},")
    print("           {'role': 'user', 'content': '请解答以下选择题:\\n" + extracted_text.replace('\n', '\\n') + "'}")
    print("       ]")
    print("   )")
    
    # 模拟模型回答
    print("\n   模型回答:")
    print("   第1题: 人工智能的英文缩写是什么？")
    print("   答案: A. AI")
    print("   解析: AI是Artificial Intelligence的缩写，即人工智能。")
    print("\n   第2题: Python是一种什么类型的编程语言？")
    print("   答案: B. 解释型")
    print("   解析: Python是一种解释型编程语言，代码在运行时逐行解释执行。")
    
    print("\n" + "=" * 40)
    print("OCR与大模型答题演示完成！")
    print("生成的截图文件: sample_questions.png")

if __name__ == "__main__":
    asyncio.run(ocr_and_model_demo())