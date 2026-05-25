from langchain.agents import create_agent, AgentState
from langchain.tools import tool, ToolRuntime
from langgraph.checkpoint.memory import InMemorySaver

from init_llm import ark_llm

class CustomAgentState(AgentState):
    name: str
    hobby: list

checkpointer = InMemorySaver()

@tool
def get_user_info(runtime: ToolRuntime) -> str:
    """
    获取用户信息
    """
    print("runtime", runtime)
    user_id = runtime.state.get("user_id")
    hobby = runtime.state.get("hobby")

    return f"用户ID: {user_id} 的爱好是{hobby}"

agent = create_agent(
    model=ark_llm,
    tools=[get_user_info],
    checkpointer=checkpointer,
    state_schema=CustomAgentState
)

config = {"configurable": {"thread_id": "session01"}}

resp1 = agent.invoke({
    "messages": [{"role": "user", "content": "我叫钱生，你是谁？"}],
    "user_id": "123",
    "hobby": ["篮球", "足球"]
}, config = config)
print(resp1["messages"][-1].content)

print("-"*50)

resp2 = agent.invoke({"messages": [{"role": "user","content": "给我查询我的信息"}]}, config = config)
print(resp2["messages"][-1].content)

print("-"*50)

state = agent.get_state(config)
print(state)
