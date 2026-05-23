from langchain_core.tools import tool
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from init_llm import ark_llm

@tool
def get_stock_price(company: str) -> str:
    """
    获取指定公司的股票价格信息
    
    Args:
        company: 公司名称，如"苹果"、"谷歌"、"微软"等
    
    Returns:
        股票价格信息字符串
    """
    stock_data = {
        "苹果": "当前股价: $178.50, 上周涨幅: +2.3%, 市值: 2.8万亿",
        "谷歌": "当前股价: $141.80, 上周涨幅: +1.5%, 市值: 1.8万亿",
        "微软": "当前股价: $378.90, 上周涨幅: +3.1%, 市值: 2.9万亿",
        "亚马逊": "当前股价: $178.20, 上周涨幅: +0.8%, 市值: 1.7万亿",
        "特斯拉": "当前股价: $248.50, 上周涨幅: -1.2%, 市值: 0.8万亿",
    }
    
    for key in stock_data:
        if key in company:
            return f"{company}的股票信息: {stock_data[key]}"
    
    return f"未找到{company}的股票信息，请确认公司名称是否正确"


@tool
def search_news(keyword: str) -> str:
    """
    搜索指定关键词的新闻信息
    
    Args:
        keyword: 搜索关键词，如"苹果公司"、"科技股"等
    
    Returns:
        新闻信息字符串
    """
    news_database = {
        "苹果": [
            "苹果公司发布新款iPhone，市场反响热烈",
            "苹果AI功能获得重大突破，股价上涨",
            "苹果公司宣布扩大在华投资计划"
        ],
        "谷歌": [
            "谷歌发布最新AI模型，性能超越GPT-4",
            "谷歌云业务增长强劲，营收超预期",
            "谷歌面临反垄断调查，股价承压"
        ],
        "科技": [
            "科技股整体上涨，AI概念股领涨",
            "多家科技公司发布财报，业绩超预期",
            "科技行业并购活跃，市场信心增强"
        ],
        "股价": [
            "美股科技股普遍上涨，投资者情绪乐观",
            "分析师看好科技股后市表现",
            "机构投资者加仓科技板块"
        ]
    }
    
    results = []
    for key in news_database:
        if key in keyword:
            results.extend(news_database[key])
    
    if results:
        news_list = "\n".join([f"{i+1}. {news}" for i, news in enumerate(results[:3])])
        return f"关于'{keyword}'的最新新闻:\n{news_list}"
    
    return f"未找到关于'{keyword}'的相关新闻"


agent = create_agent(
    model=ark_llm,
    tools=[get_stock_price, search_news],
    system_prompt="你是一个专业的金融分析师助手，擅长分析股票和财经新闻。"
)

if __name__ == "__main__":
    print("开始执行 Agent...")
    print("="*60)
    
    response = agent.invoke({
        "messages": [HumanMessage(content="比较一下苹果公司和谷歌公司的上周股价")]
    })
    
    print("\n" + "="*60)
    print("Agent 执行结果:")
    print("="*60)
    
    if "messages" in response:
        for message in response["messages"]:
            if hasattr(message, 'content'):
                print(f"\n{message.__class__.__name__}:")
                print(message.content)
    
    print("\n" + "="*60)
