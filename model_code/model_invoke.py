from typing import Iterator

from init_llm import ark_llm
from langchain_core.messages import AIMessageChunk

if __name__ == "__main__":
    # print(ark_llm.invoke("介绍一下你自己"))
    resp: Iterator[AIMessageChunk] = ark_llm.stream("使用20个字给我介绍什么是大模型？")
    for chunk in resp:
        # print(chunk,type(chunk))
        # end=""避免打印时自动换行，flush=TrUe及时刷新输出
        print(chunk.content,end="|",flush=True)
