from langchain.agents import create_agent, AgentState
from langchain.agents.middleware.types import before_model, after_model
from langchain.tools import tool, ToolRuntime
from langgraph.checkpoint.memory import InMemorySaver
from langchain.agents.middleware import SummarizationMiddleware

from init_llm import ark_llm

checkpointer = InMemorySaver()

@tool
def get_weather(city: str) -> str:
    """
    获取城市的天气
    """
    return f"{city}的天气是晴朗的"

@before_model
def before_model(state: AgentState, runtime: ToolRuntime) -> dict | None:
    """
    在模型调用前执行
    """
    print("before_model_state", state)

    messages = state["messages"]

    return {"messages": messages}

@after_model
def after_model(state: AgentState, runtime: ToolRuntime) -> dict | None:
    """
    在模型调用后执行
    """
    print("after_model_state", state)

    messages = state["messages"]

    return {"messages": messages}

agent = create_agent(
    model=ark_llm,
    tools=[get_weather],
    checkpointer=checkpointer,
    middleware=[
        before_model,
        after_model,
        SummarizationMiddleware(
            model=ark_llm,
            trigger=("messages", 5),
            keep=("messages", 2),
            summary_prompt="请摘要以下内容: {messages}"
        )
    ]
)

config = {"configurable": {"thread_id": "session01"}}

resp1 = agent.invoke({
    "messages": [{"role": "user", "content": "我叫钱生，你是谁？"}]
}, config = config)
print(resp1["messages"][-1].content)

print("-"*50)

resp2 = agent.invoke({"messages": [{"role": "user","content": "今天深圳的天气如何?"}]}, config = config)
print(resp2["messages"][-1].content)

print("-"*50)

resp3 = agent.invoke({"messages": [{"role": "user","content": "我的名字叫什么?"}]}, config = config)
print(resp3["messages"][-1].content)
