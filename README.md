# Dolphin LangChain Project

基于 LangChain 和 LangGraph 的智能体开发框架，提供完整的 Agent、工具、记忆管理等功能。

## 项目结构

```
dolphin-langchain/
├── agent_code/              # Agent 智能体示例
│   └── agent_code.py        # 金融分析师 Agent
├── deep_agent_code/         # 深度 Agent 示例
│   └── deep_agent.py        # 高级 Agent 功能
├── memory_code/             # 记忆与状态管理
│   ├── memory_code.py       # 内存记忆示例
│   ├── memory_db_code.py    # MySQL 数据库记忆
│   ├── memory_context.py    # 中间件(Middleware)示例
│   ├── memory_custom_code.py # 自定义状态示例
│   ├── memory_custom_use.py  # Command 状态更新
│   ├── long_term_memory.py  # 长期记忆
│   └── long_term_memory_db.py # 数据库长期记忆
├── model_code/              # 模型调用示例
│   ├── model_invoke.py      # 基础模型调用
│   └── struct_output.py     # 结构化输出
├── tool_code/               # 工具定义与调用
│   └── tool_call.py         # 工具调用示例
├── pdf2md/                  # PDF 工具
│   └── pdf_to_markdown.py   # PDF 转 Markdown
├── init_llm.py              # LLM 初始化配置
├── env_utils.py             # 环境变量工具
├── pyproject.toml           # 项目配置
├── requirements.txt         # 依赖列表
└── .env_example             # 环境变量示例
```

## 快速开始

### 1. 环境准备

```bash
# 克隆项目
git clone <repository-url>
cd dolphin-langchain

# 创建虚拟环境
python -m venv .venv

# 激活虚拟环境
# Windows
.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 2. 配置环境变量

复制 `.env_example` 为 `.env` 并填写配置：

```bash
cp .env_example .env
```

编辑 `.env` 文件：

```env
ARK_API_KEY=your_api_key_here
ARK_BASE_URL=https://api.example.com/v1
```

### 3. 运行示例

```bash
# 运行 Agent 示例
python agent_code/agent_code.py

# 运行记忆管理示例
python memory_code/memory_code.py

# 运行工具调用示例
python tool_code/tool_call.py

# PDF 转 Markdown
python pdf2md/pdf_to_markdown.py input.pdf -o output.md
```

## 功能模块

### 1. Agent 智能体 (agent_code)

创建具有工具调用能力的智能体：

```python
from langchain.agents import create_agent
from langchain_core.tools import tool

@tool
def get_stock_price(company: str) -> str:
    """获取股票价格"""
    return f"{company}的股价信息"

agent = create_agent(
    model=ark_llm,
    tools=[get_stock_price],
    system_prompt="你是一个金融分析师助手"
)

response = agent.invoke({"messages": [...]})
```

### 2. 记忆管理 (memory_code)

#### 内存记忆

```python
from langgraph.checkpoint.memory import InMemorySaver

checkpointer = InMemorySaver()
agent = create_agent(
    model=ark_llm,
    checkpointer=checkpointer
)
```

#### 数据库记忆

```python
from langgraph.checkpoint.mysql.pymysql import PyMySQLSaver

DB_URI = "mysql+pymysql://user:pass@localhost/db"
with PyMySQLSaver.from_conn_string(DB_URI) as checkpointer:
    checkpointer.setup()
    agent = create_agent(model=ark_llm, checkpointer=checkpointer)
```

#### 中间件 (Middleware)

```python
from langchain.agents.middleware import SummarizationMiddleware
from langchain.agents.middleware.types import before_model, after_model

@before_model
def before_hook(state, runtime):
    print("模型调用前")
    return None

agent = create_agent(
    model=ark_llm,
    middleware=[
        before_hook,
        SummarizationMiddleware(
            model=ark_llm,
            trigger=("messages", 5),
            keep=("messages", 2)
        )
    ]
)
```

### 3. 工具定义 (tool_code)

```python
from langchain_core.tools import tool

@tool
def get_weather(city: str) -> str:
    """
    获取城市天气
    
    Args:
        city: 城市名称
    Returns:
        天气信息
    """
    return f"{city}的天气是晴朗的"

# 绑定工具到模型
model_with_tools = ark_llm.bind_tools([get_weather])
```

### 4. 结构化输出 (model_code)

```python
from pydantic import BaseModel, Field

class Person(BaseModel):
    name: str = Field(description="姓名")
    age: int = Field(description="年龄")
    email: str = Field(description="邮箱")

model_with_struct = ark_llm.with_structured_output(Person)
result = model_with_struct.invoke("介绍一个25岁的张三")
print(result.name, result.age, result.email)
```

### 5. PDF 转 Markdown (pdf2md)

```python
from pdf2md import convert_pdf_to_markdown

# 转换并返回文本
markdown_text = convert_pdf_to_markdown("document.pdf")

# 转换并保存到文件
convert_pdf_to_markdown("document.pdf", output_path="output.md")
```

命令行使用：

```bash
python pdf2md/pdf_to_markdown.py document.pdf -o output.md
```

## 核心依赖

| 包名 | 用途 |
|------|------|
| langchain | LangChain 核心库 |
| langchain-core | 核心组件和接口 |
| langchain-openai | OpenAI 集成 |
| langgraph | 状态图和持久化 |
| langgraph-checkpoint-mysql | MySQL 检查点存储 |
| markitdown[pdf] | PDF 转 Markdown |

完整依赖见 `requirements.txt`。

## VS Code 配置

推荐安装以下 VS Code 扩展：

- Python (ms-python.python)
- Pylance (ms-python.vscode-pylance)
- Ruff (charliermarsh.ruff)
- Black Formatter (ms-python.black-formatter)

配置文件已包含在 `.vscode/` 目录中。

### 快捷键

| 快捷键 | 功能 |
|--------|------|
| `Ctrl+Shift+I` | 组织导入 |
| `Ctrl+.` | 快速修复 |
| `Ctrl+Space` | 触发建议 |
| `Alt+Shift+F` | 格式化代码 |
| `F5` | 启动调试 |

## API 参考

### 关键导入路径

```python
# Agent 创建
from langchain.agents import create_agent

# 工具
from langchain.tools import tool, ToolRuntime

# 状态管理
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.checkpoint.mysql.pymysql import PyMySQLSaver

# Command (状态更新)
from langgraph.types import Command

# Middleware
from langchain.agents.middleware import SummarizationMiddleware
from langchain.agents.middleware.types import before_model, after_model

# 消息类型
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
```

## 常见问题

### Q: 导入错误 `ModuleNotFoundError`

确保已安装所有依赖：

```bash
pip install -r requirements.txt
```

### Q: MySQL 字符集冲突

使用修复脚本重建数据库：

```python
import pymysql

conn = pymysql.connect(host='localhost', user='root', password='123456')
with conn.cursor() as cur:
    cur.execute("DROP DATABASE IF EXISTS langchain_db")
    cur.execute("CREATE DATABASE langchain_db CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci")
conn.close()
```

### Q: ToolRuntime 导入错误

正确的导入路径：

```python
from langchain.tools import ToolRuntime  # ✅
# 不是
from langchain_core.tools import ToolRuntime  # ❌
```

### Q: Command 导入错误

正确的导入路径：

```python
from langgraph.types import Command  # ✅
# 不是
from langgraph import Command  # ❌
```

## 开发指南

### 添加新的工具

1. 在 `tool_code/` 目录创建工具文件
2. 使用 `@tool` 装饰器定义工具
3. 在 Agent 中注册工具

### 添加新的记忆存储

1. 选择合适的 Checkpointer
2. 配置数据库连接
3. 传递给 `create_agent`

### 添加中间件

1. 使用装饰器 `@before_model` 或 `@after_model`
2. 或使用内置中间件如 `SummarizationMiddleware`
3. 在 `middleware` 参数中注册

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！

## 更新日志

### v0.1.0 (2024-05)

- 初始版本
- 支持 Agent 创建和工具调用
- 支持内存和数据库记忆
- 支持 Middleware 中间件
- 支持 PDF 转 Markdown
