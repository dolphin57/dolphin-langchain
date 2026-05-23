from langchain_core.tools import tool
from langchain_core.messages import HumanMessage,AIMessage,ToolMessage
from init_llm import ark_llm

# 1.定义工具
@tool
def get_weather(city:str)->str:
    """
    获取指定城市的天气信息

    Args:
        city (str): 城市名称
    Returns:
        str: 天气信息
    """
    return f"当前天气在{city}:晴朗，25摄氏度"

# 2.绑定工具到LLM
model_with_tools = ark_llm.bind_tools([get_weather])

if __name__=="__main__":
    # 3.与LLM对话，获取工具调用请求
    messages=[HumanMessage(content="请介绍北京的天气")]

    resp=model_with_tools.invoke(messages)
    print("LLM响应：", resp.content if hasattr(resp,'content')else resp)

    # 4.手动调用工具
    if hasattr(resp,'tool_calls')and resp.tool_calls:
        # 将A工响应加入消息
        messages.append(resp)

        for tool_call in resp.tool_calls:
            if tool_call["name"]=="get_weather":
                # 调用工具，获取结果
                tool_result = get_weather.invoke({"city":tool_call["args"]["city"]})
                print("工具结果：", tool_result)

                # 创建并添加ToolMessage
                tool_message = ToolMessage( 
                    content=tool_result,
                    tool_call_id=tool_call["id"]
                )
                messages.append(tool_message)
        
        # 5. LLM生成最终回复
        final_resp=model_with_tools.invoke(messages)
        print("最终响应：", final_resp.content if hasattr(final_resp,'content')else final_resp)
    else:
        print("LLM 没有调用工具请求")