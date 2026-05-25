from ast import NamedExpr
from langchain.agents import create_agent, AgentState
from langchain.tools import tool, ToolRuntime
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import Command
from langchain.messages import ToolMessage

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
    name = runtime.state.get("name")
    hobby = runtime.state.get("hobby")

    return f"用户名称: {name} 的爱好是{hobby}"

@tool
def update_user_info(name:str,hobby:list,runtime:ToolRuntime) -> Command:
    """更新用户信息
    Args:
        name: 用户名
        hobby: 爱好列表
    Returns:
        Command: 更新用户信息
    """
    print("runtime", runtime)
    
    if not name or not hobby:
        return Command(
            update={
                "messages":[
                    ToolMessage(
                        content="缺少用户名或爱好!",
                        tool_call_id=runtime.tool_call_id
                    )
                ]
            }
        )
    
    update = {
        "name": name,
        "hobby": hobby,
        "messages": [
            ToolMessage(
                content=f"用户{name}的爱好更新为{hobby}!",
                tool_call_id=runtime.tool_call_id
            )
        ]
    }

    return Command(update=update)

agent = create_agent(
    model=ark_llm,
    tools=[get_user_info,update_user_info],
    system_prompt="你是一个用户信息管理助手,你可以获取和更新用户信息。如果用户要求更新用户信息,请使用update_user_info工具。",
    checkpointer=checkpointer,
    state_schema=CustomAgentState
)

config = {"configurable": {"thread_id": "session01"}}

resp1 = agent.invoke({
    "messages": [{"role": "user", "content": "我叫钱生，你是谁？"}],
    "name": "dolphin",
    "hobby": ["篮球", "足球"]
}, config = config)
print(resp1["messages"][-1].content)

print("-"*50)

resp2 = agent.invoke({"messages": [{"role": "user","content": "我叫钱亮，我的爱好还有跑步"}]}, config = config)
print(resp2["messages"][-1].content)

print("-"*50)

resp3 = agent.invoke({"messages": [{"role": "user","content": "请打印我的信息"}]}, config = config)
print(resp3["messages"][-1].content)
