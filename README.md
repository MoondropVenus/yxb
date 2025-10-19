# DrissionPage MCP Server -- 骚神出品

基于DrissionPage和FastMCP的浏览器自动化MCP服务器，提供丰富的浏览器操作API供AI调用。

## 项目简介
![logo](img/DrissionPageMCP-logo.png)

DrissionPage MCP  是一个基于 DrissionPage 和 FastMCP 的浏览器自动化MCP server服务器，它提供了一系列强大的浏览器操作 API，让您能够轻松通过AI实现网页自动化操作。

### 主要特性

- 支持浏览器的打开、关闭和连接管理
- 提供丰富的页面元素操作方法
- 支持 JavaScript 代码执行
- 支持 CDP 协议操作
- 提供便捷的文件下载功能
- 支持键盘按键模拟
- 支持页面截图功能
- 支持页面文字内容提取
- 支持页面结构信息获取
- 增加 网页后台监听数据包的功能
- 增加自动上传下载文件功能

#### Python要求
- Python >= 3.9
- pip（最新版本）
- uv （最新版本）


#### 浏览器要求
- Chrome 浏览器（推荐 90 及以上版本）


#### 必需的Python包
- drissionpage >= 4.1.0.18
- fastmcp >= 2.4.0
- uv

## 安装说明
- 把本仓库git clone到本地，核心文件是main.py：
- 首先要进行[💖MCP安装环境准备工作](./MCP安装教程.md)

### 安装到Cursor编辑器

![安装说明](img/install_to_Cursor1.png)
![安装说明](img/install_to_cursor2.png)

### 安装到vscode编辑器

![安装说明](img/install_to_vscode0.png)
![安装说明](img/install_to_vscode1.png)
![安装说明](img/install_to_vscode2.png)


请将以下配置代码粘贴到编辑器的`mcpServers`设置中（请填写`你自己电脑上 main.py 文件的绝对路径`）：

```json
{
  "mcpServers": {
    "DrissionPageMCP": {
      "type": "stdio",
      "command": "uv",
      "args": ["--directory", "D:\\test10\\DrissionPageMCP", "run", "main.py"]
    }
  }
}
```
新增mcp配置 ，填写下面的配置：
``` json
"DrissionPageMCP": {
      "type": "stdio",
      "command": "uv",
      "args": ["--directory", "D:\\test10\\DrissionPageMCP", "run", "main.py"]
    } 
```

注意事项：
- 请根据实际路径修改`args`中的路径
- Windows中路径中的反斜杠需要转义（使用`\\`）
- 确保`uv`命令在系统PATH中可用
- [《MCP安装参考教程》](https://docs.trae.ai/ide/model-context-protocol)


## 调试命令

调试
```
npx -y @modelcontextprotocol/inspector uv run D:\\test10\\DrissionPageMCP\\main.py
```
或者
```
mcp dev  D:\\test10\\DrissionPageMCP\\main.py
```

## 使用示例

### 基本功能演示

运行示例脚本来查看 DrissionPageMCP 的基本功能：

```bash
uv run python example_usage.py
```

该示例演示了以下功能：
- 连接或打开浏览器
- 打开新标签页并访问网站
- 获取页面 DOM 树
- 在搜索框中输入内容
- 点击搜索按钮
- 等待页面加载
- 获取页面文本内容
- 获取当前标签页信息
- 截图并保存

### 网页截图与文字提取演示

运行专门的截图和OCR示例脚本：

```bash
uv run python screenshot_ocr_example.py
```

该示例演示了以下功能：
- 网页截图并保存为图片文件
- 从网页中提取文字内容
- 获取页面结构信息
- 处理多个不同类型的网页

### OCR文字识别与大模型答题演示

运行OCR与大模型集成示例脚本：

```bash
uv run python ocr_model_example.py
```

该示例演示了以下功能：
- 网页截图并保存为图片文件
- 从图片中提取文字内容（模拟OCR）
- 使用大模型解答选择题
- 集成魔搭ModelScope API进行推理

### 魔搭ModelScope API集成演示

运行魔搭API集成示例脚本：

```bash
uv run python modelscope_api_example.py
```

该示例演示了以下功能：
- 配置魔搭ModelScope API客户端
- 使用Qwen/Qwen3-Coder-30B-A3B-Instruct模型
- 向大模型提问选择题并获取答案
- 处理API响应和错误情况

### 完整集成示例（截图->OCR->AI答题）

运行完整的集成示例脚本：

```bash
uv run python complete_integration_example.py
```

该示例演示了完整的从网页截图到AI答题的流程：
- 使用DrissionPage打开网页并截图
- 从截图中提取题目文字内容
- 调用魔搭ModelScope API解答选择题
- 保存结果到文件供后续使用

### 在线考试题目解答

运行在线考试题目解答脚本：

```bash
uv run python solve_online_exam.py
```

该示例专门用于解答指定在线考试网站的题目：
- 自动访问指定的在线考试页面
- 自动循环答题，点击"下一题"按钮继续答题
- 截图保存每道题目的页面
- 提取题目文字内容
- 调用魔搭ModelScope API解答题目并生成详细解析
- 保存每道题的结果到文件供后续使用

注意：脚本中已配置了可用的ModelScope API密钥，可直接使用。如果您想使用自己的API密钥，可以在环境变量中设置`MODELSCOPE_API_KEY`。

## 更新日志
### v0.1.8
- 添加了自动答题功能，可自动点击"下一题"按钮循环答题
- 改进了结果保存机制，支持多题目分别保存
- 增强了答题过程的可视化和进度跟踪

### v0.1.7
- 修复了ModelScope API认证问题，现在可以正常使用AI解答功能
- 优化了在线考试题目解答脚本的稳定性

### v0.1.6
- 添加了在线考试题目解答功能，可直接解答指定网站的考试题目
- 增强了页面内容提取功能，提高了准确性

### v0.1.5
- 添加了完整的集成示例，实现从网页截图到AI答题的完整流程
- 添加了魔搭ModelScope API集成示例
- 完善了OCR文字识别与大模型答题功能

### v0.1.4
- 增加使用示例脚本
- 完善 README 文档

### v0.1.3
增加 自动上传下载文件功能
### v0.1.2
增加 网页后台监听数据包的功能

### v0.1.0

- 初始版本发布
- 实现基本的浏览器控制功能
- 提供元素操作 API
