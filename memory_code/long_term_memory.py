from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.store.memory import InMemoryStore
from langchain.tools import tool, ToolRuntime

from init_llm import ark_llm

checkpointer = InMemorySaver()
store=InMemoryStore()

store.put(
    ("dolphin",),
    "user_123",
    {"name": "张三", "age": 21, "city": "上海", "hobby": ["篮球", "足球"]}
)

store.put(
    ("dolphin",),
    "user_456",
    {"name": "钱生", "age": 20, "city": "北京", "hobby": ["篮球", "足球"]}
)

@tool
def get_user_info(runtime: ToolRuntime) -> str:
    """
    获取用户信息
    """
    store = runtime.store

    user_id = "user_123"
    user_info = store.get(("dolphin",), user_id)

    if user_info:
        print("user_info", user_info)
        value = user_info.value
        return f"用户名称: {value['name']} 的爱好是{value['hobby']}"
    else:
        return "用户不存在"

agent = create_agent(
    model=ark_llm,
    tools=[get_user_info],
    system_prompt="你是一个专业的用户信息查询助手，你可以根据调用get_user_info函数获取用户信息",
    checkpointer=checkpointer, # 短期记忆存储
    store=store # 长期记忆存储
)

config1 = {"configurable": {"thread_id": "session01"}}
config2 = {"configurable": {"thread_id": "session02"}}

resp1 = agent.invoke({"messages": [{"role": "user", "content": "获取我的信息"}]}, config = config1)
print(resp1["messages"][-1].content)

print("-"*50)

resp2 = agent.invoke({"messages": [{"role": "user","content": "获取我的信息"}]}, config = config2)
print(resp2["messages"][-1].content)