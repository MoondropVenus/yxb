#!/usr/bin/env python3
"""
在线考试题目解答脚本 - 智谱AI BigModel版本
专门用于解答 https://www.zlbbda.com.cn/studysome/topicbank 上的题目
使用智谱AI BigModel API
"""

import asyncio
import base64
from pathlib import Path
import os

# 尝试导入DrissionPage，如果没有则提示安装
try:
    from DrissionPage import ChromiumOptions, Chromium
except ImportError:
    print("请先安装DrissionPage: pip install DrissionPage")
    exit(1)

# 尝试导入zai-sdk，如果没有则提示安装
try:
    from zai import ZhipuAiClient
except ImportError:
    print("请先安装zai-sdk: pip install zai-sdk")
    exit(1)


async def connect_to_browser():
    """连接到浏览器"""
    print("1. 正在连接浏览器...")
    try:
        # 首先尝试连接到现有的浏览器实例
        co = ChromiumOptions()
        co.set_local_port(9222)  # 默认端口
        browser = Chromium(co)
        print(f"   浏览器连接成功: 127.0.0.1:9222")
        return browser
    except Exception as e:
        print(f"   连接现有浏览器失败: {e}")
        print("   正在启动新的浏览器实例...")
        try:
            # 启动新的浏览器实例
            co = ChromiumOptions()
            co.set_local_port(9222)
            co.headless(False)  # 非无头模式，方便调试
            browser = Chromium(co)
            print(f"   新浏览器启动成功: 127.0.0.1:9222")
            return browser
        except Exception as e:
            print(f"   启动新浏览器失败: {e}")
            return None


async def navigate_to_exam_page(browser):
    """导航到考试页面 - 使用当前已打开的页面"""
    print("2. 使用当前已打开的答题页面...")
    try:
        # 获取当前活动的标签页（不重新打开页面）
        tab = browser.latest_tab
        print("   使用当前页面成功")
        return tab
    except Exception as e:
        print(f"   使用当前页面失败: {e}")
        return None


async def wait_for_page_load(tab, timeout=10):
    """等待页面加载完成"""
    print("3. 等待页面加载...")
    try:
        # 等待页面加载完成
        await asyncio.sleep(timeout)
        print("   页面加载完成")
        return True
    except Exception as e:
        print(f"   等待页面加载时出错: {e}")
        return False


async def take_screenshot(tab, filename="bigmodel_exam.png"):
    """截图考试页面"""
    print("4. 正在截图考试页面...")
    try:
        # 截图整个页面
        screenshot_path = Path(filename).resolve()
        tab.get_screenshot(path=str(screenshot_path))
        print(f"   考试页面截图保存成功: {screenshot_path}")
        return str(screenshot_path)
    except Exception as e:
        print(f"   截图失败: {e}")
        return None


async def extract_text_content(tab):
    """提取页面文字内容"""
    print("5. 正在提取题目文字内容...")
    try:
        # 获取页面文本内容
        text_content = tab.html
        # 简化内容，只保留文本
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(text_content, 'html.parser')
        # 移除script和style标签
        for script in soup(["script", "style"]):
            script.decompose()
        # 获取纯文本
        text = soup.get_text()
        # 清理文本
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        
        print("   提取的题目内容:")
        # 只显示前1000个字符
        print(f"   {text[:1000]}...")
        return text
    except Exception as e:
        print(f"   提取文字内容失败: {e}")
        return None


async def extract_question_and_options(tab):
    """提取题目和选项"""
    print("5. 正在提取题目和选项...")
    try:
        # 提取题目信息
        question_info = {}
        
        # 使用和test_current_page.py相同的完整页面提取方法
        # 获取页面HTML
        html_content = tab.html
        
        # 使用BeautifulSoup解析HTML
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # 移除script和style标签
        for script in soup(["script", "style"]):
            script.decompose()
        
        # 获取纯文本
        text = soup.get_text()
        
        # 清理文本
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        clean_text = ' '.join(chunk for chunk in chunks if chunk)
        
        # 保存完整的题目内容
        question_info['question'] = clean_text
        
        # 查找选项
        options = []
        # 查找所有可能的选项元素
        option_elements = tab.eles('t:*')
        for element in option_elements:
            text = element.text.strip()
            # 检查是否为A选项（正确/正确答案等）
            if text.startswith('A') and ('正确' in text or '对' in text):
                options.append({'text': text, 'element': element})
            # 检查是否为B选项（错误/错误答案等）
            elif text.startswith('B') and ('错误' in text or '错' in text):
                options.append({'text': text, 'element': element})
        
        question_info['options'] = options
        
        print(f"   题目长度: {len(clean_text)} 字符")
        print(f"   题目预览: {clean_text[:200]}...")
        print(f"   选项: {[opt['text'] for opt in options]}")
        
        return question_info
    except Exception as e:
        print(f"   提取题目和选项失败: {e}")
        return None


def call_bigmodel_api(question_text):
    """调用智谱AI BigModel API解答问题"""
    print("6. 正在使用智谱AI解答问题...")
    try:
        # 配置智谱AI BigModel API
        api_key = "58c16dcd18a243788f32cafa7928d64f.Cglq3ehd3s7agRBe"
        client = ZhipuAiClient(api_key=api_key)
        
        # 构造更严格的提示词，只要求返回答案
        prompt = f"""
        题目：
        {question_text}
        
        请直接回答正确的答案和选项，不需要任何解释或其他内容。
        """
        
        # 调用模型 - 使用智谱AI的GLM-4.6模型
        response = client.chat.completions.create(
            model="glm-4.6",
            messages=[
                {
                    "role": "system",
                    "content": "只返回答案和选项"
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.1,  # 降低温度以获得更确定的答案
            max_tokens=5       # 限制输出长度
        )
        
        # 获取回答
        answer = response.choices[0].message.content.strip()
        print(f"\n智谱AI回答: {answer}")
        
        # 清理答案，只保留A或B
        if 'A' in answer:
            answer = 'A'
        elif 'B' in answer:
            answer = 'B'
        
        return answer, ""  # 返回答案和空的解析
    except Exception as e:
        print(f"   智谱AI解答失败: {e}")
        # 不提供默认答案，返回None表示解答失败
        print(f"\n智谱AI解答失败，不提供默认答案")
        return None, ""


def save_results(screenshot_path, extracted_text, model_answer):
    """保存结果到文件"""
    print("7. 正在保存结果到文件...")
    try:
        # 保存题目内容
        with open("bigmodel_exam_content.txt", "w", encoding="utf-8") as f:
            f.write("考试题目内容:\n")
            f.write("=" * 50 + "\n")
            f.write(extracted_text if extracted_text else "未能提取到题目内容")
        
        # 保存AI答案
        with open("bigmodel_exam_answers.txt", "w", encoding="utf-8") as f:
            f.write("考试题目:\n")
            f.write("=" * 50 + "\n")
            f.write(extracted_text if extracted_text else "未能提取到题目内容")
            f.write("\n\n智谱AI答案:\n")
            f.write("=" * 50 + "\n")
            f.write(model_answer if model_answer else "未能获得智谱AI答案")
        
        print("   结果已保存到:")
        print("   - bigmodel_exam_content.txt (题目内容)")
        print("   - bigmodel_exam_answers.txt (题目和答案)")
        if screenshot_path:
            print(f"   - {os.path.basename(screenshot_path)} (考试页面截图)")
    except Exception as e:
        print(f"   保存结果失败: {e}")


async def auto_solve_exam(browser, tab):
    """自动解答考试题目"""
    print("6. 开始自动解答考试题目...")
    
    # 获取总题数
    total_questions = 148  # 根据页面显示设置总题数
    question_count = 0
    
    # 循环处理所有题目
    while question_count < total_questions:
        question_count += 1
        print(f"\n正在处理第 {question_count} 题...")
        
        # 等待用户按回车键开始识别当前题目
        if question_count > 1:
            input(f"请手动选择答案并点击下一题，完成后按回车键开始识别第 {question_count} 题...")
        else:
            input(f"请按回车键开始识别第 {question_count} 题...")
        
        # 等待页面加载
        await asyncio.sleep(3)
        
        # 提取题目和选项
        question_info = await extract_question_and_options(tab)
        if not question_info:
            print("无法提取题目信息，跳过此题")
            # 等待用户手动操作
            input("请手动处理此题，完成后按回车键继续...")
            continue
        
        # 调用智谱AI解答问题
        question_text = question_info.get('question', '')
        print("正在调用智谱AI解答问题...")
        ai_answer, ai_explanation = call_bigmodel_api(question_text)
        if ai_answer:
            print(f"智谱AI答案: {ai_answer}")
        else:
            print("智谱AI解答失败")
        
        # 保存结果并在终端输出题目和答案
        print(f"\n{'='*50}")
        print(f"第 {question_count} 题:")
        print(f"{'='*50}")
        print(f"题目: {question_text}")
        if ai_answer:
            print(f"答案: {ai_answer}")
        if ai_explanation:
            print(f"解析: {ai_explanation}")
        print(f"{'='*50}\n")
        
        # 保存结果
        save_single_result(question_count, question_text, ai_answer, ai_explanation)
        
        # 如果是最后一题，显示完成信息
        if question_count >= total_questions:
            print("所有题目已处理完成！")
    
    print(f"\n自动答题完成，共处理 {question_count} 道题目")


def save_single_result(question_number, question_content, ai_answer, ai_explanation):
    """保存单个题目的结果（仅输出到终端，不保存文件）"""
    print(f"7. 第 {question_number} 题结果（仅显示在终端）:")
    
    try:
        # 只在终端显示题目和答案，不保存到文件
        print(f"{'='*50}")
        print(f"第 {question_number} 题:")
        print(f"{'='*50}")
        print(f"题目: {question_content[:500]}")
        if ai_answer:
            print(f"答案: {ai_answer}")
        if ai_explanation:
            print(f"解析: {ai_explanation}")
        print(f"{'='*50}\n")
            
        print(f"   第 {question_number} 题结果已显示在终端")
    except Exception as e:
        print(f"   处理第 {question_number} 题结果时出错: {e}")


async def main():
    """主函数"""
    print("开始在线考试题目解答流程（智谱AI BigModel版本）...")
    
    # 1. 连接到浏览器
    browser = await connect_to_browser()
    if not browser:
        return
    
    try:
        # 2. 导航到考试页面
        tab = await navigate_to_exam_page(browser)
        if not tab:
            print("无法打开考试页面")
            return
        
        # 3. 等待页面加载完成
        await wait_for_page_load(tab, 5)
        
        # 4. 截图考试页面
        screenshot_path = await take_screenshot(tab)
        
        # 5. 提取页面文字内容
        extracted_text = await extract_text_content(tab)
        
        # 6. 自动解答考试题目
        await auto_solve_exam(browser, tab)
        
        # 7. 保存最终结果
        if extracted_text:
            save_results(screenshot_path, extracted_text, "智谱AI答案已显示在终端")
        
        print("\n答题完成")
        
    except Exception as e:
        print(f"执行过程中发生错误: {e}")
    finally:
        # 8. 不再关闭浏览器连接，保持浏览器打开
        print("浏览器连接保持打开状态")


if __name__ == "__main__":
    # 安装必要的依赖
    try:
        import DrissionPage
        from zai import ZhipuAiClient
        import bs4
    except ImportError as e:
        print("正在安装必要的依赖包...")
        os.system("uv pip install DrissionPage zai-sdk beautifulsoup4")
    
    # 运行主程序
    asyncio.run(main())