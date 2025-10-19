#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
完整集成示例：网页截图 -> OCR文字提取 -> 大模型答题
演示完整的从网页截图到AI答题的流程
"""

import asyncio
import sys
import os

# 添加当前目录到 Python 路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main import DrissionPageMCP

def install_openai_package():
    """安装openai包（如果尚未安装）"""
    try:
        import openai
        return True
    except ImportError:
        print("正在安装openai包...")
        import subprocess
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "openai"])
            return True
        except subprocess.CalledProcessError:
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
            api_key='ms-0f3fca09-39fd-4b3b-84b8-74243108fe9e'  # 使用您提供的API密钥
        )
        
        # 构造消息
        messages = [
            {
                "role": "system",
                "content": "你是一个智能答题助手，请根据题目选择正确答案并给出解析。回答格式：答案: [选项] 解析: [解析内容]"
            },
            {
                "role": "user",
                "content": f"请解答以下选择题:\n{question_text}"
            }
        ]
        
        # 调用API
        response = client.chat.completions.create(
            model='Qwen/Qwen3-Coder-30B-A3B-Instruct',  # 使用指定的模型
            messages=messages,
            stream=False,
            temperature=0.1,  # 降低随机性，使答案更稳定
            max_tokens=500  # 限制回答长度
        )
        
        # 提取回答
        answer = response.choices[0].message.content
        return answer
        
    except Exception as e:
        return f"调用API时出错: {str(e)}"

async def complete_integration_demo():
    """完整集成演示"""
    print("完整集成演示：网页截图 -> OCR文字提取 -> 大模型答题")
    print("=" * 60)
    
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
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>在线考试系统</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 30px; background-color: #f5f5f5; }
            .exam-container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
            h1 { color: #333; text-align: center; }
            .question { margin-bottom: 25px; padding: 20px; border-left: 4px solid #4CAF50; background-color: #f9f9f9; }
            .question-title { font-size: 18px; font-weight: bold; margin-bottom: 15px; color: #333; }
            .options { margin-left: 20px; }
            .option { margin-bottom: 10px; }
            .option input { margin-right: 10px; }
        </style>
    </head>
    <body>
        <div class="exam-container">
            <h1>计算机科学基础考试</h1>
            
            <div class="question">
                <div class="question-title">1. 下列哪种数据结构遵循"后进先出"(LIFO)的原则？</div>
                <div class="options">
                    <div class="option"><input type="radio" name="q1" value="A"> A. 队列</div>
                    <div class="option"><input type="radio" name="q1" value="B"> B. 栈</div>
                    <div class="option"><input type="radio" name="q1" value="C"> C. 链表</div>
                    <div class="option"><input type="radio" name="q1" value="D"> D. 二叉树</div>
                </div>
            </div>
            
            <div class="question">
                <div class="question-title">2. HTTP协议默认使用的端口号是多少？</div>
                <div class="options">
                    <div class="option"><input type="radio" name="q2" value="A"> A. 21</div>
                    <div class="option"><input type="radio" name="q2" value="B"> B. 25</div>
                    <div class="option"><input type="radio" name="q2" value="C"> C. 80</div>
                    <div class="option"><input type="radio" name="q2" value="D"> D. 443</div>
                </div>
            </div>
            
            <div class="question">
                <div class="question-title">3. 在Python中，以下哪个关键字用于定义函数？</div>
                <div class="options">
                    <div class="option"><input type="radio" name="q3" value="A"> A. def</div>
                    <div class="option"><input type="radio" name="q3" value="B"> B. function</div>
                    <div class="option"><input type="radio" name="q3" value="C"> C. func</div>
                    <div class="option"><input type="radio" name="q3" value="D"> D. define</div>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    
    # 保存为文件
    with open("exam_questions.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    
    file_url = f"file:///{os.path.abspath('exam_questions.html').replace('\\', '/')}"
    
    try:
        result = await mcp.new_tab(file_url)
        print(f"   考试页面打开成功: {result['title']}")
    except Exception as e:
        print(f"   考试页面打开失败: {e}")
        return
    
    # 3. 等待页面加载
    print("\n3. 等待页面加载...")
    mcp.wait(2)
    
    # 4. 截图并保存
    print("\n4. 正在截图考试页面...")
    try:
        screenshot_path = mcp.get_current_tab_screenshot_as_file(".", "exam_screenshot.png")
        print(f"   考试页面截图保存成功: {screenshot_path}")
    except Exception as e:
        print(f"   考试页面截图保存失败: {e}")
        return
    
    # 5. 获取页面文本内容（模拟OCR文字提取）
    print("\n5. 正在提取题目文字内容...")
    try:
        body_text = mcp.get_body_text()
        extracted_text = str(body_text['body_text'])
        
        # 简单处理提取的文本，保留题目相关部分
        lines = extracted_text.split('\n')
        filtered_lines = [line for line in lines if line.strip() and not line.strip().startswith(('在线考试系统', '计算机科学基础考试'))]
        questions_text = '\n'.join(filtered_lines[:20])  # 取前20行
        
        print("   提取的题目内容:")
        print("   " + "\n   ".join(questions_text.split('\n')[:10]))  # 显示前10行
        print("   ...")
    except Exception as e:
        print(f"   题目文字提取失败: {e}")
        return
    
    # 6. 使用魔搭API解答问题
    print("\n6. 正在使用魔搭ModelScope API解答问题...")
    model_answer = get_model_answer_with_modelscope(questions_text)
    
    print("\n模型回答:")
    print(model_answer)
    
    # 7. 保存结果到文件
    print("\n7. 正在保存结果到文件...")
    try:
        with open("exam_answers.txt", "w", encoding="utf-8") as f:
            f.write("考试题目:\n")
            f.write(questions_text)
            f.write("\n\n模型答案:\n")
            f.write(model_answer)
        print("   结果已保存到: exam_answers.txt")
    except Exception as e:
        print(f"   保存结果失败: {e}")
    
    print("\n" + "=" * 60)
    print("完整集成演示完成！")
    print("生成的文件:")
    print("  - exam_screenshot.png (考试页面截图)")
    print("  - exam_answers.txt (题目和答案)")

if __name__ == "__main__":
    asyncio.run(complete_integration_demo())