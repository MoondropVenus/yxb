#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
网页截图与OCR文字提取示例
演示如何使用 DrissionPageMCP 进行网页截图和文字提取
"""

import asyncio
import sys
import os

# 添加当前目录到 Python 路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main import DrissionPageMCP

async def screenshot_and_ocr_demo():
    """网页截图与OCR文字提取演示"""
    print("网页截图与OCR文字提取演示")
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
    
    # 2. 打开百度图片网站作为示例
    print("\n2. 正在打开百度图片网站...")
    try:
        result = await mcp.new_tab("https://image.baidu.com/")
        print(f"   页面打开成功: {result['title']}")
    except Exception as e:
        print(f"   页面打开失败: {e}")
        return
    
    # 3. 等待页面加载
    print("\n3. 等待页面加载...")
    mcp.wait(3)
    
    # 4. 截图并保存
    print("\n4. 正在截图并保存...")
    try:
        screenshot_path = mcp.get_current_tab_screenshot_as_file(".", "baidu_image_page.png")
        print(f"   截图保存成功: {screenshot_path}")
    except Exception as e:
        print(f"   截图保存失败: {e}")
    
    # 5. 打开另一个网站演示不同类型的截图
    print("\n5. 正在打开新闻网站...")
    try:
        result = await mcp.new_tab("https://news.baidu.com/")
        print(f"   页面打开成功: {result['title']}")
    except Exception as e:
        print(f"   页面打开失败: {e}")
        return
    
    # 6. 等待页面加载
    print("\n6. 等待页面加载...")
    mcp.wait(3)
    
    # 7. 截取新闻页面并保存
    print("\n7. 正在截取新闻页面...")
    try:
        screenshot_path = mcp.get_current_tab_screenshot_as_file(".", "baidu_news_page.png")
        print(f"   新闻页面截图保存成功: {screenshot_path}")
    except Exception as e:
        print(f"   新闻页面截图保存失败: {e}")
    
    # 8. 获取页面文本内容
    print("\n8. 正在提取页面文本内容...")
    try:
        body_text = mcp.get_body_text()
        # 仅显示前500个字符
        text_preview = str(body_text['body_text'])[:500] + "..." if len(str(body_text['body_text'])) > 500 else str(body_text['body_text'])
        print(f"   页面文本提取成功，前500个字符预览:")
        print(f"   {text_preview}")
    except Exception as e:
        print(f"   页面文本提取失败: {e}")
    
    # 9. 获取简化DOM树
    print("\n9. 正在获取页面结构信息...")
    try:
        dom_tree = mcp.getSimplifiedDomTree()
        print(f"   DOM树获取成功，结构信息预览:")
        # 显示DOM树的部分结构
        dom_str = str(dom_tree)
        dom_preview = dom_str[:500] + "..." if len(dom_str) > 500 else dom_str
        print(f"   {dom_preview}")
    except Exception as e:
        print(f"   DOM树获取失败: {e}")
    
    print("\n" + "=" * 40)
    print("截图与文字提取演示完成！")
    print("生成的截图文件:")
    print("  - baidu_image_page.png")
    print("  - baidu_news_page.png")

if __name__ == "__main__":
    asyncio.run(screenshot_and_ocr_demo())