from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver

from init_llm import ark_llm

checkpointer = InMemorySaver()

agent = create_agent(
    model=ark_llm,
    tools=[],
    checkpointer=checkpointer
)

config = {"configurable": {"thread_id": "session01"}}

resp1 = agent.invoke({"messages": [{"role": "user", "content": "我叫钱生，你是谁？"}]}, config = config)
print(resp1["messages"][-1].content)

print("-"*50)

# 这次是知道叫张三的
resp2 = agent.invoke({"messages": [{"role": "user","content": "我叫什么名字？"}]}, config = config)
print(resp2["messages"][-1].content)

print("-"*50)

# 换了session就不知道了
resp2 = agent.invoke({"messages": [{"role": "user","content": "我叫什么名字？"}]}, config = {"configurable":{"thread_id":"seesion02"}})
print(resp2["messages"][-1].content)
