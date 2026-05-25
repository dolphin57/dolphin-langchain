from langchain.agents import create_agent
from langgraph.checkpoint.mysql.pymysql import PyMySQLSaver

from init_llm import ark_llm

DB_URI = "mysql+pymysql://root:123456@localhost:3306/langchain_db?charset=utf8mb4&collation=utf8mb4_general_ci"

with PyMySQLSaver.from_conn_string(DB_URI) as checkpointer:
    checkpointer.setup()

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
