#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
DrissionPageMCP 使用示例
演示如何使用 DrissionPageMCP 进行网页自动化操作
"""

import asyncio
import sys
import os

# 添加当前目录到 Python 路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main import DrissionPageMCP

async def main():
    """主函数，演示 DrissionPageMCP 的基本用法"""
    print("DrissionPageMCP 使用示例")
    print("=" * 40)
    
    # 创建 MCP 实例
    mcp = DrissionPageMCP()
    
    # 1. 获取版本信息
    version = mcp.get_version()
    print(f"1. MCP 版本: {version}")
    
    # 2. 连接或打开浏览器
    print("\n2. 正在连接或打开浏览器...")
    try:
        browser_info = await mcp.connect_or_open_browser({
            "debug_port": 9222,  # 默认调试端口
            "headless": True     # 无头模式运行
        })
        print(f"   浏览器连接成功: {browser_info['browser_address']}")
        print(f"   当前标签页标题: {browser_info['latest_tab_title']}")
    except Exception as e:
        print(f"   浏览器连接失败: {e}")
        return
    
    # 3. 打开新标签页并访问网站
    print("\n3. 正在打开百度网站...")
    try:
        result = await mcp.new_tab("https://www.baidu.com")
        print(f"   标签页打开成功")
        print(f"   页面标题: {result['title']}")
        print(f"   页面URL: {result['url']}")
    except Exception as e:
        print(f"   打开页面失败: {e}")
        return
    
    # 4. 获取页面简化 DOM 树
    print("\n4. 正在获取页面 DOM 树...")
    try:
        dom_tree = mcp.getSimplifiedDomTree()
        print(f"   DOM 树获取成功，结构示例: {str(dom_tree)[:100]}...")
    except Exception as e:
        print(f"   获取 DOM 树失败: {e}")
    
    # 5. 在搜索框中输入内容
    print("\n5. 正在搜索 '人工智能'...")
    try:
        # 使用 XPath 定位搜索框并输入内容
        input_result = mcp.input_by_xapth("//input[@id='kw']", "人工智能")
        print(f"   输入操作结果: {input_result}")
    except Exception as e:
        print(f"   输入操作失败: {e}")
    
    # 6. 点击搜索按钮
    print("\n6. 正在点击搜索按钮...")
    try:
        # 使用 XPath 定位搜索按钮并点击
        click_result = mcp.click_by_xpath("//input[@id='su']")
        print(f"   点击操作结果: {click_result}")
    except Exception as e:
        print(f"   点击操作失败: {e}")
    
    # 7. 等待页面加载
    print("\n7. 等待页面加载...")
    try:
        wait_result = mcp.wait(3)  # 等待3秒
        print(f"   等待完成: {wait_result}")
    except Exception as e:
        print(f"   等待操作失败: {e}")
    
    # 8. 获取页面文本内容
    print("\n8. 正在获取页面文本内容...")
    try:
        body_text = mcp.get_body_text()
        print(f"   页面文本获取成功，前100个字符: {str(body_text['body_text'])[:100]}...")
    except Exception as e:
        print(f"   获取页面文本失败: {e}")
    
    # 9. 获取当前标签页信息
    print("\n9. 正在获取当前标签页信息...")
    try:
        tab_info = mcp.get_current_tab_info()
        print(f"   标签页信息: {tab_info}")
    except Exception as e:
        print(f"   获取标签页信息失败: {e}")
    
    # 10. 截图并保存
    print("\n10. 正在截图并保存...")
    try:
        screenshot_path = mcp.get_current_tab_screenshot_as_file(".", "baidu_search_result.png")
        print(f"   截图保存成功: {screenshot_path}")
    except Exception as e:
        print(f"   截图保存失败: {e}")
    
    print("\n" + "=" * 40)
    print("示例演示完成！")

if __name__ == "__main__":
    asyncio.run(main())